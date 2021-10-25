#include <string.h>

#include "esp_intr_alloc.h"
#include "soc/dport_reg.h"
#include "soc/twai_struct.h"
#include "hal/twai_ll.h"
#include "driver/gpio.h"

#include "py/runtime.h"
#include "py/objstr.h"

#define DEFAULT_CAN_RX_PIN GPIO_NUM_4
#define DEFAULT_CAN_TX_PIN GPIO_NUM_5

#define BAUDRATE_1000E3 1000
#define BAUDRATE_500E3  500
#define BAUDRATE_250E3  250
#define BAUDRATE_200E3  200
#define BAUDRATE_125E3  125
#define BAUDRATE_100E3  100
#define BAUDRATE_80E3    80
#define BAUDRATE_50E3    50

typedef struct CanControllerStruct {
    void (*onReceive)(int);

    bool packetBegun;
    long txId;
    int  txExtended;
    bool txRtr;
    int  txDlc;
    int  txLength;
    int  txPin;
    uint8_t txData[8];

    long rxId;
    bool rxExtended;
    int  rxRtr;
    int  rxDlc;
    int  rxLength;
    int  rxIndex;
    int  rxPin;
    uint8_t rxData[8];

    bool loopback;
    intr_handle_t *intrHandle;
} CanController;

CanController singleton = {
    .onReceive = NULL,

    .packetBegun = false,
    .txId = -1,
    .txExtended = -1,
    .txRtr = false,
    .txDlc = 0,
    .txLength = 0,
    .txPin = DEFAULT_CAN_TX_PIN,

    .rxId = -1,
    .rxExtended = false,
    .rxRtr = false,
    .rxDlc = 0,
    .rxLength = 0,
    .rxIndex = 0,
    .rxPin = DEFAULT_CAN_RX_PIN,

    .loopback = false,
    .intrHandle = NULL,
};

void yield() {}

STATIC int begin(CanController *controller, int baudRate) {
    controller->packetBegun = false;
    controller->txId = -1;
    controller->txRtr = false;
    controller->txDlc = 0;
    controller->txLength = 0;

    controller->rxId = -1;
    controller->rxRtr = false;
    controller->rxDlc = 0;
    controller->rxLength = 0;
    controller->rxIndex = 0;

    controller->loopback = false;

    DPORT_CLEAR_PERI_REG_MASK(DPORT_PERIP_RST_EN_REG, DPORT_CAN_RST);
    DPORT_SET_PERI_REG_MASK(DPORT_PERIP_CLK_EN_REG, DPORT_CAN_CLK_EN);

    // RX pin
    gpio_set_direction(controller->rxPin, GPIO_MODE_INPUT);
    gpio_matrix_in(controller->rxPin, CAN_RX_IDX, 0);
    gpio_pad_select_gpio(controller->rxPin);

    // TX Pin
    gpio_set_direction(controller->txPin, GPIO_MODE_OUTPUT);
    gpio_matrix_out(controller->txPin, CAN_TX_IDX, 0, 0);
    gpio_pad_select_gpio(controller->txPin);
        
    // pelican mode
    twai_ll_enable_extended_reg_layout(&TWAI);

    // set bus timing
    uint32_t brp;
    uint32_t sjw = 2;
    uint32_t tseg1;
    uint32_t tseg2 = 2;
    bool triple_sampling = true;
    switch (baudRate) {
        case BAUDRATE_1000E3: tseg1 =  5; brp =  10; break;
        case BAUDRATE_500E3:  tseg1 = 13; brp =  10; break;
        case BAUDRATE_250E3:  tseg1 = 13; brp =  20; break;
        case BAUDRATE_200E3:  tseg1 = 13; brp =  26; break;
        case BAUDRATE_125E3:  tseg1 = 13; brp =  40; break;
        case BAUDRATE_100E3:  tseg1 = 13; brp =  50; break;
        case BAUDRATE_80E3:   tseg1 = 13; brp =  62; break;
        case BAUDRATE_50E3:   tseg1 = 13; brp = 100; break;
        default: return 0; break;
        //Due to limitations in ESP32 hardware and/or RTOS software, baudrate can't be lower than 50kbps.
        //See https://esp32.com/viewtopic.php?t=2142
    }
    twai_ll_set_bus_timing(&TWAI, brp, sjw, tseg1, tseg2, triple_sampling);

    // enable all interrupts
    twai_ll_set_enabled_intrs(&TWAI, 0xFF);

    // set filter to allow anything
    twai_ll_set_acc_filter(&TWAI, 0x00, 0xFF, true);

    // reset error counters
    twai_ll_set_rec(&TWAI, 0x00);
    twai_ll_set_tec(&TWAI, 0x00);

    // clear errors and interrupts
    twai_ll_clear_err_code_cap(&TWAI);
    twai_ll_get_and_clear_intrs(&TWAI);

    // normal mode
    twai_ll_set_mode(&TWAI, TWAI_MODE_NORMAL);
    twai_ll_exit_reset_mode(&TWAI);

    return 1;
}

STATIC void end(CanController *controller) {
    if (controller->intrHandle) {
        esp_intr_free(*(controller->intrHandle));
        controller->intrHandle = NULL;
    }

    DPORT_SET_PERI_REG_MASK(DPORT_PERIP_RST_EN_REG, DPORT_CAN_RST);
    DPORT_CLEAR_PERI_REG_MASK(DPORT_PERIP_CLK_EN_REG, DPORT_CAN_CLK_EN);
}

STATIC int beginPacket(CanController *controller, int id, int dlc, bool rtr) {
    if (id < 0 || id > 0x7FF) {
        return 0;
    }

    if (dlc > 8) {
        return 0;
    }

    controller->packetBegun = true;
    controller->txId = id;
    controller->txExtended = false;
    controller->txRtr = rtr;
    controller->txDlc = dlc;
    controller->txLength = 0;

    memset(controller->txData, 0x00, sizeof(controller->txData));

    return 1;
}

STATIC int beginExtendedPacket(CanController *controller, long id, int dlc, bool rtr) {
    if (id < 0 || id > 0x1FFFFFFF) {
        return 0;
    }

    if (dlc > 8) {
        return 0;
    }

    controller->packetBegun = true;
    controller->txId = id;
    controller->txExtended = true;
    controller->txRtr = rtr;
    controller->txDlc = dlc;
    controller->txLength = 0;

    memset(controller->txData, 0x00, sizeof(controller->txData));

    return 1;
}

STATIC int endPacket(CanController *controller) {
    if (!controller->packetBegun) {
        return 0;
    }
    controller->packetBegun = false;

    if (controller->txDlc >= 0) {
        controller->txLength = controller->txDlc;
    }

    // wait for TX buffer to free
    while(TWAI.status_reg.tbs != 1) {
        yield();
    }

    uint32_t flags = 0;
    if (controller->txExtended) {
        flags |= TWAI_MSG_FLAG_EXTD;
    }
    if (controller->txRtr) {
        flags |= TWAI_MSG_FLAG_RTR;
    }
    twai_ll_frame_buffer_t frame;
    twai_ll_format_frame_buffer(controller->txId, controller->txLength, &(controller->txData), flags, &frame);
    twai_ll_set_tx_buffer(&TWAI, &frame);


    if (controller->loopback) {
        // self reception request
        twai_ll_set_cmd_self_rx_request(&TWAI);
    } else {
        // transmit request
        twai_ll_set_cmd_tx(&TWAI);
    }

    // wait for TX complete
    while(TWAI.status_reg.tcs != 1) {
        if (TWAI.error_code_capture_reg.val == 0xd9) {
            // error, abort
            twai_ll_set_cmd_abort_tx(&TWAI);
            return 0;
        }
        yield();
    }

    return 1;
}

STATIC long packetId(CanController *controller) {
    return controller->rxId;
}

STATIC bool packetExtended(CanController *controller) {
    return controller->rxExtended;
}

STATIC bool packetRtr(CanController *controller) {
    return controller->rxRtr;
}

STATIC int packetDlc(CanController *controller) {
    return controller->rxDlc;
}

STATIC size_t writeBuffer(CanController *controller, const uint8_t *buffer, size_t size) {
    if (!controller->packetBegun) {
        return 0;
    }

    if (size > (sizeof(controller->txData) - controller->txLength)) {
        size = sizeof(controller->txData) - controller->txLength;
    }

    memcpy(&controller->txData[controller->txLength], buffer, size);
    controller->txLength += size;

    return size;
}

STATIC size_t write(CanController *controller, uint8_t byte) {
    return writeBuffer(controller, &byte, sizeof(byte));
}

STATIC int available(CanController *controller) {
    return (controller->rxLength - controller->rxIndex);
}

STATIC uint8_t read(CanController *controller) {
    if (!available(controller)) {
        return -1;
    }

    return controller->rxData[controller->rxIndex++];
}

STATIC int peek(CanController *controller) {
    if (!available(controller)) {
        return -1;
    }

    return controller->rxData[controller->rxIndex];
}

STATIC void setPins(CanController *controller, int rx, int tx) {
  controller->rxPin = (gpio_num_t)rx;
  controller->txPin = (gpio_num_t)tx;
}

STATIC int parsePacket(CanController *controller) {
    if (TWAI.status_reg.rbs != 1) {
        // no packet
        return 0;
    }

    twai_ll_frame_buffer_t frame;
    twai_ll_get_rx_buffer(&TWAI, &frame);
    uint8_t flags;
    twai_ll_prase_frame_buffer(&TWAI, &(controller->rxId), &(controller->rxDlc), &(controller->rxData), &flags);
    if (flags & TWAI_MSG_FLAG_RTR) {
        controller->rxRtr = true;
        controller->rxLength = 0;
    } else {
        controller->rxRtr = false;
        controller->rxLength = controller->rxDlc;
    }
    if (flags & TWAI_MSG_FLAG_EXTD) {
        controller->rxExtended = true;
    } else {
        controller->rxExtended = false;
    }
    twai_ll_set_cmd_release_rx_buffer(&TWAI);

    return controller->rxDlc;
}

STATIC int filter(CanController *controller, int id, int mask) {
    twai_ll_set_acc_filter(&TWAI, id & 0x7ff, ~(mask & 0x7ff), true);
    return 1;
}

STATIC int filterExtended(CanController *controller, long id, long mask) {
    twai_ll_set_acc_filter(&TWAI, id & 0x1FFFFFFF, ~(mask & 0x1FFFFFFF), true);
    return 1;
}

STATIC int observe(CanController *controller) {
    twai_ll_enter_reset_mode(&TWAI);
    twai_ll_set_mode(&TWAI, TWAI_MODE_LISTEN_ONLY);

    return 1;
}

STATIC int loopback(CanController *controller) {
    controller->loopback = true;

    twai_ll_enter_reset_mode(&TWAI);
    twai_ll_set_mode(&TWAI, TWAI_MODE_NO_ACK);

    return 1;
}

STATIC void onInterrupt(void* arg) {
    CanController *controller = arg;

    if (TWAI.interrupt_reg.ri) {
        // received packet, parse and call callback
        parsePacket(controller);

        controller->onReceive(available(controller));
    }
}

STATIC void setOnReceive(CanController *controller, void(*callback)(int)) {
    controller->onReceive = callback;

    if (controller->intrHandle) {
        esp_intr_free(*(controller->intrHandle));
        controller->intrHandle = NULL;
    }

    if (callback) {
        esp_intr_alloc(ETS_CAN_INTR_SOURCE, 0, onInterrupt, controller, controller->intrHandle);
    }
}

STATIC mp_obj_t _begin(mp_obj_t baudrate_obj) {
    long baudrate = mp_obj_get_int(baudrate_obj);
    bool success = begin(&singleton, baudrate);
    return mp_obj_new_bool(success);
}
STATIC MP_DEFINE_CONST_FUN_OBJ_1(begin_obj, _begin);

STATIC mp_obj_t _end() {
    end(&singleton);
    return mp_const_none;
}
STATIC MP_DEFINE_CONST_FUN_OBJ_0(end_obj, _end);

STATIC mp_obj_t _beginPacket(mp_obj_t id_obj, mp_obj_t dlc_obj, mp_obj_t rtr_obj) {
    int id = mp_obj_get_int(id_obj);
    int dlc = mp_obj_get_int(dlc_obj);
    bool rtr = mp_obj_get_int(rtr_obj);
    bool success = beginPacket(&singleton, id, dlc, rtr);
    return mp_obj_new_bool(success);
}
STATIC MP_DEFINE_CONST_FUN_OBJ_3(beginPacket_obj, _beginPacket);

STATIC mp_obj_t _beginExtendedPacket(mp_obj_t id_obj, mp_obj_t dlc_obj, mp_obj_t rtr_obj) {
    int id = mp_obj_get_int(id_obj);
    int dlc = mp_obj_get_int(dlc_obj);
    bool rtr = mp_obj_get_int(rtr_obj);
    bool success = beginExtendedPacket(&singleton, id, dlc, rtr);
    return mp_obj_new_bool(success);
}
STATIC MP_DEFINE_CONST_FUN_OBJ_3(beginExtendedPacket_obj, _beginExtendedPacket);

STATIC mp_obj_t _endPacket() {
    bool success = endPacket(&singleton);
    return mp_obj_new_bool(success);
}
STATIC MP_DEFINE_CONST_FUN_OBJ_0(endPacket_obj, _endPacket);

STATIC mp_obj_t _write(mp_obj_t byte_obj) {
    GET_STR_DATA_LEN(byte_obj, string, length)
    if (length == 0) {
        mp_raise_ValueError("got empty string");
    }
    char byte = string[0];
    size_t written = write(&singleton, byte);
    return mp_obj_new_int(written);
}
STATIC MP_DEFINE_CONST_FUN_OBJ_1(write_obj, _write);

STATIC mp_obj_t _setPins(mp_obj_t rx_obj, mp_obj_t tx_obj) {
    int rx = mp_obj_get_int(rx_obj);
    int tx = mp_obj_get_int(tx_obj);
    setPins(&singleton, rx, tx);
    return mp_const_none;
}
STATIC MP_DEFINE_CONST_FUN_OBJ_2(setPins_obj, _setPins);

STATIC mp_obj_t _parsePacket() {
    int size = parsePacket(&singleton);
    return mp_obj_new_int(size);
}
STATIC MP_DEFINE_CONST_FUN_OBJ_0(parsePacket_obj, _parsePacket);

STATIC mp_obj_t _read() {
    char byte = read(&singleton);
    return mp_obj_new_str(&byte, 1);
}
STATIC MP_DEFINE_CONST_FUN_OBJ_0(read_obj, _read);

STATIC mp_obj_t *current_callback_obj = NULL;
STATIC void _onReceive(int size) {
    if (current_callback_obj) {
        mp_call_function_1(*current_callback_obj, mp_obj_new_int(size));
    }
}
STATIC mp_obj_t _setOnReceive(mp_obj_t callback_obj) {
    if (!mp_obj_is_callable(callback_obj)) {
        mp_raise_TypeError("Argument must be callable");
    } else {
        current_callback_obj = &callback_obj;
        setOnReceive(&singleton, _onReceive);
    }
    return mp_const_none;
}
STATIC MP_DEFINE_CONST_FUN_OBJ_1(setOnReceive_obj, _setOnReceive);


// Define all properties of the module.
// Table entries are key/value pairs of the attribute name (a string)
// and the MicroPython object reference.
// All identifiers and strings are written as MP_QSTR_xxx and will be
// optimized to word-sized integers by the build system (interned strings).
STATIC const mp_rom_map_elem_t can_module_globals_table[] = {
    { MP_ROM_QSTR(MP_QSTR___name__), MP_ROM_QSTR(MP_QSTR_can) },
    { MP_ROM_QSTR(MP_QSTR_begin), MP_ROM_PTR(&begin_obj) },
    { MP_ROM_QSTR(MP_QSTR_end), MP_ROM_PTR(&end_obj) },
    { MP_ROM_QSTR(MP_QSTR_begin_packet), MP_ROM_PTR(&beginPacket_obj) },
    { MP_ROM_QSTR(MP_QSTR_begin_extended_packet), MP_ROM_PTR(&beginExtendedPacket_obj) },
    { MP_ROM_QSTR(MP_QSTR_end_packet), MP_ROM_PTR(&endPacket_obj) },
    { MP_ROM_QSTR(MP_QSTR_write), MP_ROM_PTR(&write_obj) },
    { MP_ROM_QSTR(MP_QSTR_set_pins), MP_ROM_PTR(&setPins_obj) },
    { MP_ROM_QSTR(MP_QSTR_parse_packet), MP_ROM_PTR(&parsePacket_obj) },
    { MP_ROM_QSTR(MP_QSTR_read), MP_ROM_PTR(&read_obj) },
    { MP_ROM_QSTR(MP_QSTR_set_on_receive), MP_ROM_PTR(&setOnReceive_obj) },
};
STATIC MP_DEFINE_CONST_DICT(can_module_globals, can_module_globals_table);

// Define module object.
const mp_obj_module_t can_module = {
    .base = { &mp_type_module },
    .globals = (mp_obj_dict_t *)&can_module_globals,
};

// Register the module to make it available in Python.
// Note: the "1" in the third argument means this module is always enabled.
// This "1" can be optionally replaced with a macro like MODULE_CEXAMPLE_ENABLED
// which can then be used to conditionally enable this module.
MP_REGISTER_MODULE(MP_QSTR_can, can_module, 1);
