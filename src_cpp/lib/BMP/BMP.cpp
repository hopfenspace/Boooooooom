#include <map>
#include <set>

#include <BMP.hpp>
#include <EventLoop.hpp>
#include <CAN.h>

std::map<int, std::function<void(int, bool, std::string)>> callbacks;
std::map<int, std::string> slicedTransmissions;
std::set<int> customMSGTypes;
int address;
std::set<int> reqOnly {
    RESET, INIT, START, DEFUSED, EXPLODED, REGISTER, STRIKE, DETONATE, 
    MARK_SOLVED, MARK_REACTIVATED, CHANGE_SERIAL_NO, BLACKOUT
};
std::set<int> dataOnly { CHANGE_TIMER };


void BMP::setAddress(int addr) {
    address = addr;
}

void BMP::setCallback(MSG_TYPE msgType, std::function<void(int sender, bool isRTR, std::string data)> callback) {
    callbacks.insert(std::pair<int, std::function<void(int, bool, std::string)>>(msgType, callback));
}

bool BMP::validatePacket(int msgType, bool isRTR) {
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
        addJob(millis(), [msgType, sender](){callbacks.at(msgType)(sender, true, "");});
    } else {
        // SENDER + RECEIVER + MSG_TYPE as "unique" packet identifier
        int identifier = header >> 13;

        std::string data = "";
        for (int i = 0; i < packetSize; i++) {
            data += (char)CAN.read();
        }
        //if EOT
        if((header & 0b0000000000000001000000000000) >> 12) {
            // Check if packet is part of a sliced transmission
            if(slicedTransmissions.count(identifier)) {
                std::string completeData = slicedTransmissions.at(identifier) + data;
                slicedTransmissions.erase(identifier);
                addJob(millis(), [msgType, sender, completeData](){callbacks.at(msgType)(sender, false, completeData);});
            } else {
                addJob(millis(), [msgType, sender, data](){callbacks.at(msgType)(sender, false, data);});
            }
        } else {
            if(slicedTransmissions.count(identifier)) {
                slicedTransmissions.at(identifier) += data;
            } else {
                slicedTransmissions.insert(std::pair<int, std::string>(identifier, data));
            }
        }
    }
}

void BMP::begin(long baudrate) {
    CAN.begin(baudrate);
    CAN.onReceive(BMP::processInterrupt);
}