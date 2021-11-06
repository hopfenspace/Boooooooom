#ifndef BMP_HPP_
#define BMP_HPP_

#include <functional>
#include <vector>

enum MSG_TYPE {
    RESET = 0, INIT = 1, START = 2, DEFUSED = 3, EXPLODED = 4, RTFM = 5, VERSION = 6, MODULE_INFO = 7, 
    REGISTER = 8, STRIKE = 9, DETONATE = 10, MARK_SOLVED = 11, MARK_REACTIVATED = 12, CHANGE_TIMER = 13,
    CHANGE_SERIAL_NO = 14,  TIMER = 15, SERIAL_NO = 16, STRIKES = 17, MAX_STRIKES = 18, MODULE_COUNT = 19, 
    ACTIVE_MODULE_COUNT = 20, DIFFICULTY = 21, LABELS = 22, BLACKOUT = 23, IS_SOLVED = 24
};

class BMP {
    public:
        static void begin(long baudrate);
        static void setAddress(uint8_t addr);
        static void setCallback(uint8_t msgType, std::function<void(uint8_t sender, bool isRTR, std::vector<uint8_t> data)> callback);
        static void registerCustomMSGType(uint8_t msgType);
        static void reqRESET(uint8_t dst);
        static void reqINIT(uint8_t dst);
        static void reqSTART(uint8_t dst);
        static void reqDEFUSED(uint8_t dst);
        static void reqEXPLODED(uint8_t dst);
        static void reqRTFM(uint8_t dst);
        static void sendRTFM(std::string);
        static void reqVERSION(uint8_t dst);
        static void sendVERSION(uint8_t dst, uint8_t version);
        static void reqMODULE_INFO(uint8_t dst);
        static void sendMODULE_INFO(uint8_t dst, std::vector<uint8_t> data);
        static void reqREGISTER();
        static void reqSTRIKE();
        static void reqDETONATE();
        static void reqMARK_SOLVED();
        static void reqMARK_REACTIVATED();
        static void sendCHANGE_TIMER(int32_t deltaTime);
        static void reqCHANGE_SERIAL_NO();
        static void reqTIMER();
        static void sendTIMER(uint8_t dst, uint32_t timer);
        static void reqSERIAL_NO();
        static void sendSERIAL_NO(uint8_t dst, std::string);
        static void reqSTRIKES();
        static void sendSTRIKES(uint8_t dst, uint8_t strikes);
        static void reqMAX_STRIKES();
        static void sendMAX_STRIKES(uint8_t dst, uint8_t maxStrikes);
        static void reqMOUDLE_COUNT();
        static void sendMODULE_COUNT(uint8_t dst, uint8_t moduleCount);
        static void reqACTIVE_MODULE_COUNT();
        static void sendACTIVE_MODULE_COUNT(uint8_t dst, uint8_t activeModuleCount);
        static void reqDIFFICULTY();
        static void sendDIFFICULTY(uint8_t dst, uint8_t difficulty);
        static void reqLABELS();
        static void sendLABELS(uint8_t dst, std::map<std::string, bool> labels);
        static void reqBLACKOUT(uint8_t dst);
        static void reqIS_SOLVED(uint8_t dst);
        static void sendIS_SOLVED(uint8_t dst, bool isSolved);
    private:
        static long constructPacketId(uint8_t dst, MSG_TYPE msgType, bool isSliced = false);
        static void processInterrupt(int packetSize);
        static bool validatePacket(uint8_t msgType, bool isRTR);
};

#endif