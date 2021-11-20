#include <string.h>

#include "driver/gpio.h"
#include "hal/twai_hal.h"
#include "driver/twai.h"

#include "py/runtime.h"
#include "py/objstr.h"

#define BAUDRATE_1000E3 1000
#define BAUDRATE_800E3   800
#define BAUDRATE_500E3   500
#define BAUDRATE_250E3   250
#define BAUDRATE_125E3   125
#define BAUDRATE_100E3   100
#define BAUDRATE_50E3     50
#define BAUDRATE_25E3     25

MP_DEFINE_EXCEPTION(EspError, OSError)
MP_DEFINE_EXCEPTION(EspTimeoutError, EspError)
MP_DEFINE_EXCEPTION(EspStateError, EspError)
#define ESP_ERR_CASE(error, string) case error: {char message[] = string; arg = mp_obj_new_str(message, strlen(message)); break;}
#define ESP_ERR_CASE_EXCEPT(error, string, exception_name) case error: {char message[] = string; arg = mp_obj_new_str(message, strlen(message)); exception = &mp_type_##exception_name; break;}
STATIC void raise_esp_err(esp_err_t error) {
    const mp_obj_type_t *exception = &mp_type_EspError;
    mp_obj_t arg;
    switch (error) {
        case ESP_OK: return;
        ESP_ERR_CASE(ESP_FAIL, "Generic ESP Error")

        ESP_ERR_CASE(ESP_ERR_NO_MEM, "Out of memory")
        ESP_ERR_CASE(ESP_ERR_INVALID_ARG, "Invalid argument")
        ESP_ERR_CASE_EXCEPT(ESP_ERR_INVALID_STATE, "Invalid state", EspStateError)
        ESP_ERR_CASE(ESP_ERR_INVALID_SIZE, "Invalid size")
        ESP_ERR_CASE(ESP_ERR_NOT_FOUND, "Requested resource not found")
        ESP_ERR_CASE(ESP_ERR_NOT_SUPPORTED, "Operation or feature not supported")
        ESP_ERR_CASE_EXCEPT(ESP_ERR_TIMEOUT, "Operation timed out", EspTimeoutError)
        ESP_ERR_CASE(ESP_ERR_INVALID_RESPONSE, "Received response was invalid")
        ESP_ERR_CASE(ESP_ERR_INVALID_CRC, "CRC or checksum was invalid")
        ESP_ERR_CASE(ESP_ERR_INVALID_VERSION, "Version was invalid")
        ESP_ERR_CASE(ESP_ERR_INVALID_MAC, "MAC address was invalid")

        ESP_ERR_CASE(ESP_ERR_WIFI_BASE, "Starting number of WiFi error codes")
        ESP_ERR_CASE(ESP_ERR_MESH_BASE, "Starting number of MESH error codes")
        ESP_ERR_CASE(ESP_ERR_FLASH_BASE, "Starting number of flash error codes")

        default: {char message[] = "Undocumented error"; arg = mp_obj_new_str(message, strlen(message)); break;}
    }
    mp_raise_type_arg(exception, arg);
}
#define ESP_ERR_RAISE_RETURN(error) {esp_err_t temp = error; if (temp != ESP_OK) {raise_esp_err(temp); return mp_const_none;}}

STATIC void interupt_handler(void *arg);


twai_general_config_t general = TWAI_GENERAL_CONFIG_DEFAULT(5, 4, TWAI_MODE_NORMAL);
twai_timing_config_t timing;
twai_filter_config_t filter = TWAI_FILTER_CONFIG_ACCEPT_ALL();

#define BAUDRATE_CASE(in, out) case in: {twai_timing_config_t temp = out(); timing = temp; break;}
STATIC mp_obj_t start(mp_obj_t baudrate_obj) {
    switch (mp_obj_get_int(baudrate_obj)) {
        BAUDRATE_CASE(BAUDRATE_1000E3, TWAI_TIMING_CONFIG_1MBITS)
        BAUDRATE_CASE(BAUDRATE_800E3, TWAI_TIMING_CONFIG_800KBITS)
        BAUDRATE_CASE(BAUDRATE_500E3, TWAI_TIMING_CONFIG_500KBITS)
        BAUDRATE_CASE(BAUDRATE_250E3, TWAI_TIMING_CONFIG_250KBITS)
        BAUDRATE_CASE(BAUDRATE_125E3, TWAI_TIMING_CONFIG_125KBITS)
        BAUDRATE_CASE(BAUDRATE_100E3, TWAI_TIMING_CONFIG_100KBITS)
        BAUDRATE_CASE(BAUDRATE_50E3, TWAI_TIMING_CONFIG_50KBITS)
        BAUDRATE_CASE(BAUDRATE_25E3, TWAI_TIMING_CONFIG_25KBITS)
        default: mp_raise_ValueError("invalid baudrate"); break;
    }
    set_handler_extension(interupt_handler);
    general.rx_queue_len = 20;
    ESP_ERR_RAISE_RETURN(twai_driver_install(&general, &timing, &filter));
    ESP_ERR_RAISE_RETURN(twai_start());
    return mp_const_none;
}
STATIC MP_DEFINE_CONST_FUN_OBJ_1(start_obj, start);

STATIC mp_obj_t stop() {
    ESP_ERR_RAISE_RETURN(twai_stop());
    ESP_ERR_RAISE_RETURN(twai_driver_uninstall());
    return mp_const_none;
}
STATIC MP_DEFINE_CONST_FUN_OBJ_0(stop_obj, stop);

STATIC mp_obj_t set_pins(mp_obj_t tx, mp_obj_t rx) {
    general.rx_io = mp_obj_get_int(rx);
    general.tx_io = mp_obj_get_int(tx);
    return mp_const_none;
}
STATIC MP_DEFINE_CONST_FUN_OBJ_2(set_pins_obj, set_pins);

STATIC mp_obj_t transmit(size_t nargs, const mp_obj_t *args) {//id, ext, rtr, dlc || data
    twai_message_t msg;
    msg.identifier = mp_obj_get_int(args[0]);
    msg.extd = mp_obj_get_int(args[1]);
    msg.rtr = mp_obj_get_int(args[2]);
    if (msg.rtr) {
        msg.data_length_code = mp_obj_get_int(args[3]);
    } else {
        GET_STR_DATA_LEN(args[3], string, length);
        msg.data_length_code = MIN(length, 8);
        for (int i = 0; i < msg.data_length_code; i++) {
            msg.data[i] = string[i];
        }
    }
    ESP_ERR_RAISE_RETURN(twai_transmit(&msg, pdMS_TO_TICKS(10)));
    return mp_const_none;
}
STATIC MP_DEFINE_CONST_FUN_OBJ_VAR(transmit_obj, 4, transmit);

STATIC mp_obj_t receive() {
    twai_message_t msg;
    ESP_ERR_RAISE_RETURN(twai_receive(&msg, 0));
    mp_obj_t items[4];
    items[0] = mp_obj_new_int(msg.identifier);
    items[1] = mp_obj_new_bool(msg.extd);
    items[2] = mp_obj_new_bool(msg.rtr);
    if (msg.rtr) {
	    items[3] = mp_obj_new_int(msg.data_length_code);
    } else {
	    char data[8];
	    for (int i = 0; i < msg.data_length_code; i++) {
		data[i] = (char) msg.data[i];
	    }
	    items[3] = mp_obj_new_str(data, msg.data_length_code);
    }
    return mp_obj_new_tuple(4, items);
}
STATIC MP_DEFINE_CONST_FUN_OBJ_0(receive_obj, receive);

STATIC mp_obj_t callback = NULL;
STATIC mp_obj_t collect(mp_obj_t arg) {
    twai_message_t msg;
    esp_err_t result = twai_receive(&msg, 0);
    if (result == ESP_OK) {
        mp_obj_t list = mp_obj_new_list(0, NULL);
        mp_obj_t items[4];
        while (result == ESP_OK) {
            // Add message to list
            items[0] = mp_obj_new_int(msg.identifier);
            items[1] = mp_obj_new_bool(msg.extd);
            items[2] = mp_obj_new_bool(msg.rtr);
            if (msg.rtr) {
                items[3] = mp_obj_new_int(msg.data_length_code);
            } else {
                char data[8];
                for (int i = 0; i < msg.data_length_code; i++) {
                data[i] = (char) msg.data[i];
                }
                items[3] = mp_obj_new_str(data, msg.data_length_code);
            }
            mp_obj_list_append(list, mp_obj_new_tuple(4, items));

            // Get next message
            result = twai_receive(&msg, 0);
        }
        // Hand list of messages to user callback
        mp_call_function_1(callback, list);
    }
    // Timeout is default exit, everything else is broken
    if (result != ESP_ERR_TIMEOUT) raise_esp_err(result);
    return mp_const_none;
}
STATIC MP_DEFINE_CONST_FUN_OBJ_1(collect_obj, collect);
STATIC void interupt_handler(void *arg) {
    uint32_t event = *(uint32_t*)arg;
    if ((callback != NULL) && (event & TWAI_HAL_EVENT_RX_BUFF_FRAME)) {
        mp_sched_schedule(MP_OBJ_FROM_PTR(&collect_obj), mp_const_none);
    }
}
STATIC mp_obj_t onReceive(mp_obj_t callback_obj) {
    callback = callback_obj;
    return mp_const_none;
}
STATIC MP_DEFINE_CONST_FUN_OBJ_1(onReceive_obj, onReceive);

// Define all properties of the module.
// Table entries are key/value pairs of the attribute name (a string)
// and the MicroPython object reference.
// All identifiers and strings are written as MP_QSTR_xxx and will be
// optimized to word-sized integers by the build system (interned strings).
STATIC const mp_rom_map_elem_t can_module_globals_table[] = {
    { MP_ROM_QSTR(MP_QSTR___name__), MP_ROM_QSTR(MP_QSTR_can) },
    { MP_ROM_QSTR(MP_QSTR_start), MP_ROM_PTR(&start_obj) },
    { MP_ROM_QSTR(MP_QSTR_stop), MP_ROM_PTR(&stop_obj) },
    { MP_ROM_QSTR(MP_QSTR_transmit), MP_ROM_PTR(&transmit_obj) },
    { MP_ROM_QSTR(MP_QSTR_receive), MP_ROM_PTR(&receive_obj) },
    { MP_ROM_QSTR(MP_QSTR_on_receive), MP_ROM_PTR(&onReceive_obj) },
    { MP_ROM_QSTR(MP_QSTR_set_pins), MP_ROM_PTR(&set_pins_obj) },
    { MP_ROM_QSTR(MP_QSTR_EspError), MP_ROM_PTR(&mp_type_EspError) },
    { MP_ROM_QSTR(MP_QSTR_EspStateError), MP_ROM_PTR(&mp_type_EspStateError) },
    { MP_ROM_QSTR(MP_QSTR_EspTimeoutError), MP_ROM_PTR(&mp_type_EspTimeoutError) },
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
