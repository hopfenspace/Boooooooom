#include <map>
#include <set>
#include <iterator>

#include <BMP.hpp>
#include <EventLoop.hpp>
#include <CAN.h>

#define MASTER_DEVICE 0

std::map<uint8_t, std::function<void(uint8_t, bool, std::vector<uint8_t>)>> callbacks;
std::map<uint8_t, std::vector<uint8_t>> slicedTransmissions;
std::set<int> customMSGTypes;
uint8_t address;
std::set<uint8_t> reqOnly {
    RESET, INIT, START, DEFUSED, EXPLODED, REGISTER, STRIKE, DETONATE, 
    MARK_SOLVED, MARK_REACTIVATED, CHANGE_SERIAL_NO, BLACKOUT
};
std::set<uint8_t> dataOnly { CHANGE_TIMER };



void BMP::setAddress(uint8_t addr) {
    address = addr;
}

long BMP::constructPacketId(uint8_t dst, MSG_TYPE msgType, bool isSliced) {
    return ((((((address << 4) + dst) << 8) + msgType) << 1) + (int)!isSliced) << 12;
}

void BMP::reqRESET(uint8_t dst) {
    CAN.beginExtendedPacket(BMP::constructPacketId(dst, RESET), -1, true);
    CAN.endPacket();
}

void BMP::reqINIT(uint8_t dst) {
    CAN.beginExtendedPacket(BMP::constructPacketId(dst, INIT), -1, true);
    CAN.endPacket();
}

void BMP::reqSTART(uint8_t dst) {
    CAN.beginExtendedPacket(BMP::constructPacketId(dst, START), -1, true);
    CAN.endPacket();
}

void BMP::reqDEFUSED(uint8_t dst) {
    CAN.beginExtendedPacket(BMP::constructPacketId(dst, DEFUSED), -1, true);
    CAN.endPacket();
}

void BMP::reqEXPLODED(uint8_t dst) {
    CAN.beginExtendedPacket(BMP::constructPacketId(dst, EXPLODED), -1, true);
    CAN.endPacket();
}

void BMP::reqRTFM(uint8_t dst) {
    CAN.beginExtendedPacket(BMP::constructPacketId(dst, RTFM), -1, true);
    CAN.endPacket();
}

void BMP::sendRTFM(std::string manual) {
    for(int i = 0; i < manual.length(); i++) {
        if(i%8 == 0) {
            if(manual.length() - 1 - i < 8) {
                CAN.beginExtendedPacket(BMP::constructPacketId(MASTER_DEVICE, RTFM));
            } else {
                CAN.beginExtendedPacket(BMP::constructPacketId(MASTER_DEVICE, RTFM, true));
            }
        }
        CAN.write((char)manual[i]);
        if(i%8 == 7 || i == manual.length() - 1) {
            CAN.endPacket();
        }
    }
}

void BMP::reqVERSION(uint8_t dst) {
    CAN.beginExtendedPacket(BMP::constructPacketId(dst, VERSION), -1, true);
    CAN.endPacket();
}

void BMP::sendVERSION(uint8_t dst, uint8_t version) {
    CAN.beginExtendedPacket(BMP::constructPacketId(dst, VERSION));
    CAN.write((char)version);
    CAN.endPacket();
}

void BMP::reqMODULE_INFO(uint8_t dst) {
    CAN.beginExtendedPacket(BMP::constructPacketId(dst, MODULE_INFO), -1, true);
    CAN.endPacket();
}

void BMP::sendMODULE_INFO(uint8_t dst, std::vector<uint8_t> data) {
    for(int i = 0; i < data.size(); i++) {
        if(i%8 == 0) {
            if(data.size() - 1 - i < 8) {
                CAN.beginExtendedPacket(BMP::constructPacketId(dst, MODULE_INFO));
            } else {
                CAN.beginExtendedPacket(BMP::constructPacketId(dst, MODULE_INFO, true));
            }
        }
        CAN.write(data[i]);
        if(i%8 == 7 || i == data.size() - 1) {
            CAN.endPacket();
        }
    }
}

void BMP::reqREGISTER() {
    CAN.beginExtendedPacket(BMP::constructPacketId(MASTER_DEVICE, REGISTER), -1, true);
    CAN.endPacket();
}

void BMP::reqSTRIKE() {
    CAN.beginExtendedPacket(BMP::constructPacketId(MASTER_DEVICE, STRIKE), -1, true);
    CAN.endPacket();
}

void BMP::reqDETONATE() {
    CAN.beginExtendedPacket(BMP::constructPacketId(MASTER_DEVICE, DETONATE), -1, true);
    CAN.endPacket();
}

void BMP::reqMARK_SOLVED() {
    CAN.beginExtendedPacket(BMP::constructPacketId(MASTER_DEVICE, MARK_SOLVED), -1, true);
    CAN.endPacket();
}

void BMP::reqMARK_REACTIVATED() {
    CAN.beginExtendedPacket(BMP::constructPacketId(MASTER_DEVICE, MARK_REACTIVATED), -1, true);
    CAN.endPacket();
}

void BMP::sendCHANGE_TIMER(int32_t deltaTime) {
    CAN.beginExtendedPacket(BMP::constructPacketId(MASTER_DEVICE, CHANGE_TIMER));
    for(int i = 1; i < 5; i++) {
        CAN.write(deltaTime >> i*8);
    }
    CAN.endPacket();
}

void BMP::reqCHANGE_SERIAL_NO() {
    CAN.beginExtendedPacket(BMP::constructPacketId(MASTER_DEVICE, CHANGE_SERIAL_NO), -1, true);
    CAN.endPacket();
}

void BMP::reqTIMER() {
    CAN.beginExtendedPacket(BMP::constructPacketId(MASTER_DEVICE, TIMER), -1, true);
    CAN.endPacket();
}

void BMP::sendTIMER(uint8_t dst, uint32_t timer) {
    CAN.beginExtendedPacket(BMP::constructPacketId(dst, TIMER));
    for(int i = 3; i >= 0; i--) {
        CAN.write(timer >> i*8);
    }
    CAN.endPacket();
}

void BMP::reqSERIAL_NO() {
    CAN.beginExtendedPacket(BMP::constructPacketId(MASTER_DEVICE, SERIAL_NO), -1, true);
    CAN.endPacket();
}

void BMP::sendSERIAL_NO(uint8_t dst, std::string serialNo) {
    CAN.beginExtendedPacket(BMP::constructPacketId(dst, SERIAL_NO));
    for(int i = 0; i < serialNo.length(); i++) {
        if(i >= 8) {
            break;
        }
        CAN.write((char)serialNo[i]);
    }
    CAN.endPacket();
}

void BMP::reqSTRIKES() {
    CAN.beginExtendedPacket(BMP::constructPacketId(MASTER_DEVICE, STRIKES), -1, true);
    CAN.endPacket();
}

void BMP::sendSTRIKES(uint8_t dst, uint8_t strikes) {
    CAN.beginExtendedPacket(BMP::constructPacketId(dst, STRIKES));
    CAN.write(strikes);
    CAN.endPacket();
}

void BMP::reqMAX_STRIKES() {
    CAN.beginExtendedPacket(BMP::constructPacketId(MASTER_DEVICE, MAX_STRIKES), -1, true);
    CAN.endPacket();
}
void BMP::sendMAX_STRIKES(uint8_t dst, uint8_t maxStrikes) {
    CAN.beginExtendedPacket(BMP::constructPacketId(dst, MAX_STRIKES));
    CAN.write(maxStrikes);
    CAN.endPacket();
}

void BMP::reqMOUDLE_COUNT() {
    CAN.beginExtendedPacket(BMP::constructPacketId(MASTER_DEVICE, MODULE_COUNT), -1, true);
    CAN.endPacket();
}

void BMP::sendMODULE_COUNT(uint8_t dst, uint8_t moduleCount) {
    CAN.beginExtendedPacket(BMP::constructPacketId(dst, MODULE_COUNT));
    CAN.write(moduleCount);
    CAN.endPacket();
}

void BMP::reqACTIVE_MODULE_COUNT() {
    CAN.beginExtendedPacket(BMP::constructPacketId(MASTER_DEVICE, ACTIVE_MODULE_COUNT), -1, true);
    CAN.endPacket();
}

void BMP::sendACTIVE_MODULE_COUNT(uint8_t dst, uint8_t activeModuleCount) {
    CAN.beginExtendedPacket(BMP::constructPacketId(dst, ACTIVE_MODULE_COUNT));
    CAN.write(activeModuleCount);
    CAN.endPacket();
}

void BMP::reqDIFFICULTY() {
    CAN.beginExtendedPacket(BMP::constructPacketId(MASTER_DEVICE, DIFFICULTY), -1, true);
    CAN.endPacket();
}

void BMP::sendDIFFICULTY(uint8_t dst, uint8_t difficulty) {
    CAN.beginExtendedPacket(BMP::constructPacketId(dst, DIFFICULTY));
    CAN.write(difficulty);
    CAN.endPacket();
}

void BMP::reqLABELS() {
    CAN.beginExtendedPacket(BMP::constructPacketId(MASTER_DEVICE, LABELS), -1, true);
    CAN.endPacket();
}

void BMP::sendLABELS(uint8_t dst, std::map<std::string, bool> labels) {
    std::map<std::string, bool>::iterator it = labels.begin();

    for(int i = 0; i < labels.size(); i++) {
        if(i%2 == 0) {
            if(labels.size() - 1 - i < 2) {
                CAN.beginExtendedPacket(BMP::constructPacketId(dst, LABELS));
            } else {
                CAN.beginExtendedPacket(BMP::constructPacketId(dst, LABELS, true));
            }
        }
        CAN.write(it->second);
        for(auto j : it->first) {
            CAN.write((char)j);
        }
        if(i%2 == 1 || i == labels.size() - 1) {
            CAN.endPacket();
        }
        it++;
    }
}

void BMP::reqBLACKOUT(uint8_t dst) {
    CAN.beginExtendedPacket(BMP::constructPacketId(dst, BLACKOUT), -1, true);
    CAN.endPacket();
}

void BMP::reqIS_SOLVED(uint8_t dst) {
    CAN.beginExtendedPacket(BMP::constructPacketId(dst, IS_SOLVED), -1, true);
    CAN.endPacket();
}

void BMP::sendIS_SOLVED(uint8_t dst, bool isSolved) {
    CAN.beginExtendedPacket(BMP::constructPacketId(dst, IS_SOLVED));
    CAN.write(isSolved);
    CAN.endPacket();
}

void BMP::setCallback(uint8_t msgType, std::function<void(uint8_t sender, bool isRTR, std::vector<uint8_t> data)> callback) {
    callbacks.insert(std::pair<int, std::function<void(uint8_t, bool, std::vector<uint8_t>)>>(msgType, callback));
}

bool BMP::validatePacket(uint8_t msgType, bool isRTR) {
    // REQ only
    if(reqOnly.count(msgType) > 0) {
        return isRTR ? true : false;
    }
    // Data only
    if(dataOnly.count(msgType) > 0) {
        return isRTR ? false : true;
    }

    // Everything allowed
    return true;
}

void BMP::processInterrupt(int packetSize) {
    if(!(CAN.packetExtended())) {
        return;
    }

    uint32_t header = CAN.packetId();
    if(((header & 0b0000111100000000000000000000) >> 21) != address) {
        return;
    }
    
    int msgType = (header & 0b00000000111111110000000000000) >> 13;
    if(callbacks.count(msgType) == 0 && customMSGTypes.count(msgType) == 0) {
        // No callback was registered for this MSG_TYPE
        return;
    }

    if(customMSGTypes.count(msgType) == 0) {
        if(!BMP::validatePacket(msgType, CAN.packetRtr())) {
            // MSG_TYPE and packet type incompatible
            return;
        }
    }

    int sender = (header & 0b11110000000000000000000000000) >> 25;
    if(CAN.packetRtr()) {
        // if NOT EOT; return
        if(!(header & 0b0000000000000001000000000000) >> 12) {
            return;
        }
        addJob(millis(), [msgType, sender](){callbacks.at(msgType)(sender, true, std::vector<uint8_t>());});
    } else {
        // SENDER + RECEIVER + MSG_TYPE as "unique" packet identifier
        int identifier = header >> 13;

        std::vector<uint8_t> data;

        for (int i = 0; i < packetSize; i++) {
            data.push_back((uint8_t)CAN.read());
        }
        //if EOT
        if((header & 0b0000000000000001000000000000) >> 12) {
            // Check if packet is part of a sliced transmission
            if(slicedTransmissions.count(identifier)) {
                std::vector<uint8_t> completeData = slicedTransmissions.at(identifier);
                for(auto i : data) {
                    completeData.push_back(i);
                }
                slicedTransmissions.erase(identifier);
                addJob(millis(), [msgType, sender, completeData](){callbacks.at(msgType)(sender, false, completeData);});
            } else {
                addJob(millis(), [msgType, sender, data](){callbacks.at(msgType)(sender, false, data);});
            }
        } else {
            if(slicedTransmissions.count(identifier)) {
                for(auto i : data) {
                    slicedTransmissions.at(identifier).push_back(i);
                }
            } else {
                slicedTransmissions.insert(std::pair<int, std::vector<uint8_t>>(identifier, data));
            }
        }
    }
}

void BMP::begin(long baudrate) {
    CAN.begin(baudrate);
    CAN.onReceive(BMP::processInterrupt);
}