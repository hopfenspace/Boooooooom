#ifndef BMP_HPP_
#define BMP_HPP_

#include <functional>
#include <string>

enum MSG_TYPE {
    RESET = 0, INIT = 1, START = 2, DEFUSED = 3, EXPLODED = 4, RTFM = 5, VERSION = 6, MODULE_INFO = 7, 
    REGISTER = 8, STRIKE = 9, DETONATE = 10, MARK_SOLVED = 11, MARK_REACTIVATED = 12, CHANGE_TIMER = 13,
    CHANGE_SERIAL_NO = 14,  TIMER = 15, SERIAL_NO = 16, STRIKES = 17, MAX_STRIKES = 18, MODULE_COUNT = 19, 
    ACTIVE_MODULE_COUNT = 20, DIFFICULTY = 21, LABELS = 22, BLACKOUT = 23, IS_SOLVED = 24
};

class BMP {
    public:
        static void setCallback(MSG_TYPE msgType, std::function<void(int sender, bool isRTR, std::string data)> callback);
        static void begin(long baudrate);
        static void registerCustomMSGType(uint8_t msgType);
        static void setAddress(int addr);
    private:
        static void processInterrupt(int packetSize);
        static bool validatePacket(int msgType, bool isRTR);
};

#endif