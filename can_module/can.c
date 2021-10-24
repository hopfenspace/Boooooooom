#include <string.h>

#include "esp_intr_alloc.h"
#include "soc/dport_reg.h"
#include "soc/twai_struct.h"
#include "hal/twai_ll.h"
#include "driver/gpio.h"

#include "py/runtime.h"

#define DEFAULT_CAN_RX_PIN GPIO_NUM_4
#define DEFAULT_CAN_TX_PIN GPIO_NUM_5

#define BAUDRATE_1000E3 1000
#define BAUDRATE_500E3 500
#define BAUDRATE_250E3 250
#define BAUDRATE_200E3 200
#define BAUDRATE_125E3 125
#define BAUDRATE_100E3 100
#define BAUDRATE_80E3 80
#define BAUDRATE_50E3 50

typedef struct CanControllerStruct {
    void (*onReceive)(int);

    bool packetBegun;
    long  txId;
    int  txExtended;
    bool txRtr;
    int  txDlc;
    int  txLength;
    int  txPin;
    uint8_t txData[8];

    long  rxId;
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
    TWAI.clock_divider_reg.cm = 1;  //modifyRegister(REG_CDR, 0x80, 0x80);
    // SJW = 1
    TWAI.bus_timing_0_reg.sjw = 1;  //modifyRegister(REG_BTR0, 0xc0, 0x40);
    // TSEG2 = 1
    TWAI.bus_timing_1_reg.tseg2 = 1;    //modifyRegister(REG_BTR1, 0x70, 0x10);

    switch (baudRate) {
        case BAUDRATE_1000E3:
            TWAI.bus_timing_1_reg.tseg1 = 0x04;    //modifyRegister(REG_BTR1, 0x0f, 0x04);
            TWAI.bus_timing_0_reg.brp = 4;  //modifyRegister(REG_BTR0, 0x3f, 4);
            break;

        case BAUDRATE_500E3:
            TWAI.bus_timing_1_reg.tseg1 = 0x0c;    //modifyRegister(REG_BTR1, 0x0f, 0x0c);
            TWAI.bus_timing_0_reg.brp = 4;  //modifyRegister(REG_BTR0, 0x3f, 4);
            break;

        case BAUDRATE_250E3:
            TWAI.bus_timing_1_reg.tseg1 = 0x0c;    //modifyRegister(REG_BTR1, 0x0f, 0x0c);
            TWAI.bus_timing_0_reg.brp = 9;  //modifyRegister(REG_BTR0, 0x3f, 9);
            break;

        case BAUDRATE_200E3:
            TWAI.bus_timing_1_reg.tseg1 = 0x0c;    //modifyRegister(REG_BTR1, 0x0f, 0x0c);
            TWAI.bus_timing_0_reg.brp = 12;  //modifyRegister(REG_BTR0, 0x3f, 12);
            break;

        case BAUDRATE_125E3:
            TWAI.bus_timing_1_reg.tseg1 = 0x0c;    //modifyRegister(REG_BTR1, 0x0f, 0x0c);
            TWAI.bus_timing_0_reg.brp = 19;  //modifyRegister(REG_BTR0, 0x3f, 19);
            break;

        case BAUDRATE_100E3:
            TWAI.bus_timing_1_reg.tseg1 = 0x0c;    //modifyRegister(REG_BTR1, 0x0f, 0x0c);
            TWAI.bus_timing_0_reg.brp = 24;  //modifyRegister(REG_BTR0, 0x3f, 24);
            break;

        case BAUDRATE_80E3:
            TWAI.bus_timing_1_reg.tseg1 = 0x0c;    //modifyRegister(REG_BTR1, 0x0f, 0x0c);
            TWAI.bus_timing_0_reg.brp = 30;  //modifyRegister(REG_BTR0, 0x3f, 30);
            break;

        case BAUDRATE_50E3:
            TWAI.bus_timing_1_reg.tseg1 = 0x0c;    //modifyRegister(REG_BTR1, 0x0f, 0x0c);
            TWAI.bus_timing_0_reg.brp = 49;  //modifyRegister(REG_BTR0, 0x3f, 49);
            break;

        /*
        Due to limitations in ESP32 hardware and/or RTOS software, baudrate can't be lower than 50kbps.
        See https://esp32.com/viewtopic.php?t=2142
        */
        default:
            return 0;
            break;
    }

    // SAM = 1
    TWAI.bus_timing_1_reg.sam = 1;  //modifyRegister(REG_BTR1, 0x80, 0x80);
    // enable all interrupts
    TWAI.interrupt_enable_reg.val = 255;   //writeRegister(REG_IER, 0xff);

    // set filter to allow anything
    for (int i = 0; i < 4; i++)
        TWAI.acceptance_filter.acr[i].val = 0;   //writeRegister(REG_ACRn(0..3), 0x00);
    for (int i = 0; i < 4; i++)
        TWAI.acceptance_filter.amr[i].val = 255;   //writeRegister(REG_AMRn(0..3), 0xff);

    // normal output mode
    //TWAI.reserved_20 |= 2;
    //TWAI.reserved_20 &= ~1;     //modifyRegister(REG_OCR, 0x03, 0x02);
    // reset error counters
    TWAI.tx_error_counter_reg.val = 0;   //writeRegister(REG_TXERR, 0x00);
    TWAI.rx_error_counter_reg.val = 0;   //writeRegister(REG_RXERR, 0x00);

    // clear errors and interrupts
    TWAI.error_code_capture_reg.val;    //readRegister(REG_ECC);
    TWAI.interrupt_reg.val;     //readRegister(REG_IR);

    // normal mode
    TWAI.mode_reg.afm = 1;  //modifyRegister(REG_MOD, 0x08, 0x08);
    TWAI.mode_reg.rm = 0;   //modifyRegister(REG_MOD, 0x17, 0x00);
    TWAI.mode_reg.lom = 0;  //
    TWAI.mode_reg.stm = 0;  //
    //TWAI.mode_reg.reserved4 &= ~1;

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
    while(TWAI.status_reg.tbs != 1) {   //while ((readRegister(REG_SR) & 0x04) != 0x04) {
        yield();
    }

    int dataReg;
    if (controller->txExtended) {
        TWAI.tx_rx_buffer[0].val = 0x80 | (controller->txRtr ? 0x40 : 0x00) | (0x0f & controller->txLength);  //writeRegister(REG_EFF, 0x80 | (_txRtr ? 0x40 : 0x00) | (0x0f & _txLength));
        TWAI.tx_rx_buffer[1].val = controller->txId >> 21;  //writeRegister(REG_EFF + 1, _txId >> 21);
        TWAI.tx_rx_buffer[2].val = controller->txId >> 13;  //writeRegister(REG_EFF + 2, _txId >> 13);
        TWAI.tx_rx_buffer[3].val = controller->txId >>  5;  //writeRegister(REG_EFF + 3, _txId >> 5);
        TWAI.tx_rx_buffer[4].val = controller->txId <<  3;  //writeRegister(REG_EFF + 4, _txId << 3);

        dataReg = 5;    //dataReg = REG_EFF + 5;
    } else {
        TWAI.tx_rx_buffer[0].val = (controller->txRtr ? 0x40 : 0x00) | (0x0f & controller->txLength); //writeRegister(REG_SFF, (_txRtr ? 0x40 : 0x00) | (0x0f & _txLength));
        TWAI.tx_rx_buffer[1].val = controller->txId >> 3;   //writeRegister(REG_SFF + 1, _txId >> 3);
        TWAI.tx_rx_buffer[2].val = controller->txId << 5;   //writeRegister(REG_SFF + 2, _txId << 5);

        dataReg = 3;    //dataReg = REG_SFF + 3;
    }

    for (int i = 0; i < controller->txLength; i++) {
        TWAI.tx_rx_buffer[dataReg + i].val = controller->txData[i];    //writeRegister(dataReg + i, _txData[i]);
    }

    if (controller->loopback) {
        // self reception request
        TWAI.command_reg.val &= ~0x1f;    //modifyRegister(REG_CMR, 0x1f, 0x10);
        TWAI.command_reg.srr = 1;         //
    } else {
        // transmit request
        TWAI.command_reg.val &= ~0x1f;    //modifyRegister(REG_CMR, 0x1f, 0x01);
        TWAI.command_reg.tr = 1;          //
    }

    // wait for TX complete
    while(TWAI.status_reg.tcs != 1) {   //while ((readRegister(REG_SR) & 0x08) != 0x08) {
        if (TWAI.error_code_capture_reg.val == 0xd9) {  //if (readRegister(REG_ECC) == 0xd9) {
            // error, abort
            TWAI.command_reg.val &= ~0x1f;    //modifyRegister(REG_CMR, 0x1f, 0x02);
            TWAI.command_reg.at = 1;          //
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

STATIC int read(CanController *controller) {
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
    if (TWAI.status_reg.rbs != 1) { //if ((readRegister(REG_SR) & 0x01) != 0x01) {
        // no packet
        return 0;
    }

    controller->rxExtended = (TWAI.tx_rx_buffer[0].val & 0x80) ? true : false;   //(readRegister(REG_SFF) & 0x80) ? true : false;
    controller->rxRtr = (TWAI.tx_rx_buffer[0].val & 0x40) ? true : false;   //(readRegister(REG_SFF) & 0x40) ? true : false;
    controller->rxDlc = TWAI.tx_rx_buffer[0].val & 0x0f;   //(readRegister(REG_SFF) & 0x0f);
    controller->rxIndex = 0;

    int dataReg;
    if (controller->rxExtended) {
        controller->rxId = (TWAI.tx_rx_buffer[1].val << 21) |   //(readRegister(REG_EFF + 1) << 21) |
                           (TWAI.tx_rx_buffer[2].val << 13) |   //(readRegister(REG_EFF + 2) << 13) |
                           (TWAI.tx_rx_buffer[3].val << 5) |    //(readRegister(REG_EFF + 3) << 5) |
                           (TWAI.tx_rx_buffer[4].val << 3);     //(readRegister(REG_EFF + 4) >> 3);

        dataReg = 5;    //dataReg = REG_EFF + 5;
    } else {
        controller->rxId = (TWAI.tx_rx_buffer[1].val << 3) | ((TWAI.tx_rx_buffer[2].val >> 5) & 0x07);  //(readRegister(REG_SFF + 1) << 3) | ((readRegister(REG_SFF + 2) >> 5) & 0x07);

        dataReg = 3;    //dataReg = REG_SFF + 3;
    }

    if (controller->rxRtr) {
        controller->rxLength = 0;
    } else {
        controller->rxLength = controller->rxDlc;

        for (int i = 0; i < controller->rxLength; i++) {
            controller->rxData[i] = TWAI.tx_rx_buffer[dataReg + i].val;     //readRegister(dataReg + i);
        }
    }

    // release RX buffer
    TWAI.command_reg.val &= ~0x04;    //modifyRegister(REG_CMR, 0x04, 0x04);
    TWAI.command_reg.rrb = 1;         //

    return controller->rxDlc;
}

STATIC int filter(CanController *controller, int id, int mask) {
    id &= 0x7ff;
    mask = ~(mask & 0x7ff);

    twai_ll_enter_reset_mode(&TWAI);

    TWAI.acceptance_filter.acr[0].val = id >> 3;    //writeRegister(REG_ACRn(0), id >> 3);
    TWAI.acceptance_filter.acr[1].val = id << 5;    //writeRegister(REG_ACRn(1), id << 5);
    TWAI.acceptance_filter.acr[2].val = 0x00;   //writeRegister(REG_ACRn(2), 0x00);
    TWAI.acceptance_filter.acr[3].val = 0x00;   //writeRegister(REG_ACRn(3), 0x00);

    TWAI.acceptance_filter.amr[0].val = mask >> 3;  //writeRegister(REG_AMRn(0), mask >> 3);
    TWAI.acceptance_filter.amr[1].val = (mask << 5) | 0x1f; //writeRegister(REG_AMRn(1), (mask << 5) | 0x1f);
    TWAI.acceptance_filter.amr[2].val = 0xff;   //writeRegister(REG_AMRn(2), 0xff);
    TWAI.acceptance_filter.amr[3].val = 0xff;   //writeRegister(REG_AMRn(3), 0xff);

    twai_ll_set_mode(&TWAI, TWAI_MODE_NORMAL);

    return 1;
}

STATIC int filterExtended(CanController *controller, long id, long mask) {
    id &= 0x1FFFFFFF;
    mask &= ~(mask & 0x1FFFFFFF);

    twai_ll_enter_reset_mode(&TWAI);

    TWAI.acceptance_filter.acr[0].val = id >> 21;   //writeRegister(REG_ACRn(0), id >> 21);
    TWAI.acceptance_filter.acr[1].val = id >> 13;   //writeRegister(REG_ACRn(1), id >> 13);
    TWAI.acceptance_filter.acr[2].val = id >> 5;    //writeRegister(REG_ACRn(2), id >> 5);
    TWAI.acceptance_filter.acr[3].val = id << 5;    //writeRegister(REG_ACRn(3), id << 5);

    TWAI.acceptance_filter.amr[0].val = mask >> 21; //writeRegister(REG_AMRn(0), mask >> 21);
    TWAI.acceptance_filter.amr[1].val = mask >> 13; //writeRegister(REG_AMRn(1), mask >> 13);
    TWAI.acceptance_filter.amr[2].val = mask >> 5;  //writeRegister(REG_AMRn(2), mask >> 5);
    TWAI.acceptance_filter.amr[3].val = (mask << 5) | 0x1f; //writeRegister(REG_AMRn(3), (mask << 5) | 0x1f);

    twai_ll_set_mode(&TWAI, TWAI_MODE_NORMAL);

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
    uint8_t byte = mp_obj_get_int(byte_obj);
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
    int byte = read(&singleton);
    return mp_obj_new_int(byte);
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
