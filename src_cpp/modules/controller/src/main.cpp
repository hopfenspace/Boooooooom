#include <string>
#include <set>
#include <map>

#include <Arduino.h>
#include <WiFi.h>

#include <EventLoop.hpp>
#include <BMP.hpp>

#define CAN_ADDRESS 0
/*
#define SR_0_LATCH
#define SR_0_CLK
#define SR_0_DATA

#define SR_1_LATCH
#define SR_1_CLK
#define SR_1_DATA

#define DIFF_0
#define DIFF_1
#define DIFF_2
#define DIFF_3
#define DIFF_4
#define DIFF_5
#define DIFF_6
*/

enum DIFFICULTY {IMMORTAL = 0, TRAINING = 1, EASY = 2, NORMAL = 3, HARD = 4, EXPERT = 5, PREPARE_2_DIE = 6};

const char* wifiSSID = "BOMBENKOFFER";
std::string style = R"(
<style>
body {
    margin: 1rem;
    font-family: "Bitstream Vera Sans Mono", Monaco, "Courier New", Courier, monospace;
}
</style>
)";
WiFiServer server(80);

std::set<int> addresses;
std::map<int, bool> solvedStates;
std::map<std::string, bool> labels;
std::map<uint8_t, std::string> manuals;
uint8_t maxStrikes;
uint8_t strikes = 0;
std::string serialNo;
uint8_t difficulty;
unsigned long startTime;
// 1/100s as base unit 
unsigned long currentTimer;
float timeFactor = 1.0;

void loop() {
    executeJobs(millis());
}

void setSerial() {
    std::string alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789";
    serialNo = "";
    for(int i = 0; i < 8; i++) {
        serialNo += alphabet[rand() % alphabet.length()];
    }
}

void generateLabels() {
    std::string alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
    labels.clear();

    int labelCount;
    if(difficulty < NORMAL) {
        labelCount = 0;
    } else {
        labelCount = rand() % 5;
    }

    for(int i = 0; i < labelCount; i++) {
        std::string label = "";
        for(int i = 0; i < 3; i++) {
            label += alphabet[rand() % alphabet.length()];
        }
        labels.insert(std::pair<std::string, bool>(label, rand() % 2));
    }
}

std::function<void()> calcTimer();
std::function<void()> calcTimer() {
    return [](){
        currentTimer -= (int)(10 * timeFactor);
        if(currentTimer <= 0) {
            currentTimer = 0;
            for(auto pair : solvedStates) {
                BMP::reqEXPLODED(pair.first);
            }
            return;
        }
        addJob(millis()+100, calcTimer());
    };
}

void processREGISTER(int sender, bool isRTR, std::vector<uint8_t> data) {
    if(!addresses.count(sender)) {
        addresses.insert(sender);
    }
    if(!solvedStates.count(sender)) {
        solvedStates.insert(std::pair<int, bool>(sender, false));
    }
    Serial.printf("Module %d registered\n", sender);
}

void processSTRIKE(int sender, bool isRTR, std::vector<uint8_t> data) {
    strikes++;
    if(strikes < 4) {
        timeFactor += 0.5;
    }
    if(maxStrikes == strikes) {
        for(auto address : addresses) {
            BMP::reqEXPLODED(address);
        }
    }
    Serial.printf("Module %d sent a strike\n", sender);
}

void processDETONATE(int sender, bool isRTR, std::vector<uint8_t> data) {
    for(auto address : addresses) {
        BMP::reqEXPLODED(address);
    }
    Serial.printf("Module %d sent DETONATE\n", sender);
}

void processMARK_SOLVED(int sender, bool isRTR, std::vector<uint8_t> data) {
    if(solvedStates.count(sender)) {
        solvedStates.at(sender) = true;
    }
    bool completeSolved = true;
    for(auto pair : solvedStates) {
        if(!pair.second) {
            completeSolved = false;
            break;
        }
    }
    if(completeSolved) {
        // Send DEFUSED if timer > 0
        for(auto address : addresses) {
            BMP::reqDEFUSED(address);
        }
    }
    Serial.printf("Module %d marked itself as solved\n", sender);
}

void processCHANGE_TIMER(int sender, bool isRTR, std::vector<uint8_t> data) {
    uint32_t tmp = 0;
    for(int i = 0; i < data.size(); i++) {
        tmp = (tmp << 8) + data[i];
    }
    int32_t deltaTime = (int32_t)tmp;
    // TODO Change timer
    Serial.printf("Module %d wants to change the timer: %d \n", sender, deltaTime);
}

void processCHANGE_SERIAL_NO(int sender, bool isRTR, std::vector<uint8_t> data) {
    setSerial();
    Serial.printf("Module %d requests change in serialNo, new serialNo: %s\n", sender, serialNo.c_str());
}

void processTIMER(int sender, bool isRTR, std::vector<uint8_t> data) {
    if(!isRTR) {
        return;
    }
    uint32_t curr = (unsigned long)(currentTimer/10);
    BMP::sendTIMER(sender, curr);
    Serial.printf("Module %d wants to know the timer: %u\n", sender, curr);
}

void processSERIAL_NO(int sender, bool isRTR, std::vector<uint8_t> data) {
    if(!isRTR) {
        return;
    }
    BMP::sendSERIAL_NO(sender, serialNo);
    Serial.printf("Module %d wants to know the serialNo\n", sender);
}

void processSTRIKES(int sender, bool isRTR, std::vector<uint8_t> data) {
    if(!isRTR) {
        return;
    }
    BMP::sendSTRIKES(sender, strikes);
    Serial.printf("Module %d wants to know the current number of strikes\n", sender);
}

void processMAX_STRIKES(int sender, bool isRTR, std::vector<uint8_t> data) {
    if(!isRTR) {
        return;
    }
    BMP::sendMAX_STRIKES(sender, maxStrikes);
    Serial.printf("Module %d wants to know the maximum number of strikes\n", sender);
}

void processMODULE_COUNT(int sender, bool isRTR, std::vector<uint8_t> data) {
    if(!isRTR) {
        return;
    }
    BMP::sendMODULE_COUNT(sender, solvedStates.size());
    Serial.printf("Module %d wants to know the number of available modules\n", sender);
}

void processACTIVE_MODULE_COUNT(int sender, bool isRTR, std::vector<uint8_t> data) {
    if(!isRTR) {
        return;
    }
    int unfinished = 0;
    for(auto module : solvedStates) {
        if(!module.second) {
            unfinished++;
        }
    }
    BMP::sendACTIVE_MODULE_COUNT(sender, unfinished);
    Serial.printf("Module %d wants to know the number of unfinished modules\n", sender);
}

void processDIFFICULTY(int sender, bool isRTR, std::vector<uint8_t> data) {
    if(!isRTR) {
        return;
    }
    BMP::sendDIFFICULTY(sender, difficulty);
    Serial.printf("Module %d wants to know the current difficulty\n", sender);
}

void processLABELS(int sender, bool isRTR, std::vector<uint8_t> data) {
    if(!isRTR) {
        return;
    }
    BMP::sendLABELS(sender, labels);
    Serial.printf("Module %d wants to know the defined labels\n", sender);
}

void processRTFM(int sender, bool isRTR, std::vector<uint8_t> data) {
    if(isRTR) {
        return;
    }
    std::string manual = "";
    for(int i = 0; i < data.size(); i++) {
        manual += (char)data[i];
    }
    if(manuals.count(sender)) {
        manuals.at(sender) = manual;
    } else {
        manuals.emplace(std::pair<uint8_t, std::string>(sender, manual));
    }
    Serial.printf("Module %d sent its manual: %s\n", sender, manual.c_str());
}

std::function<void()> listenWifi() {
    return [](){
        WiFiClient client = server.available();
        if(client) {
            if (client.available()) {
                client.println("HTTP/1.1 200 OK");
                client.println("Content-Type: text/html");
                client.println("Connection: close");
                client.println();
                
                client.println("<!DOCTYPE html><html lang=\"en\"><head>");
                client.println("<meta charset=\"US-ASCII\">");
                client.println("<meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">");
                client.println("<title>Bomb manual</title>");
                client.print(style.c_str());
                client.println("</head><body>");
                client.println("<h1>Bomb manual</h1>");
                client.println("<p>The following headings describe all the modules located in the bomb.</p>");
                for(auto i : manuals) {
                    client.print(i.second.c_str());
                }
                client.println("</body>");
                client.flush();
                client.stop();
            }
        }
        addJob(millis()+100, listenWifi());
    };
}

void setup() {
    Serial.begin(115200);
    Serial.println("Initialized serial");

    srand(esp_random());
    Serial.println("Use CHAOS to generate random numbers");

    difficulty = NORMAL;
    maxStrikes = 3;
    // * 100 for 1/100s
    currentTimer = 300 * 100;
    addJob(millis(), calcTimer());

    setSerial();
    Serial.printf("Generated serial_no: %s\n", serialNo.c_str());

    generateLabels();
        Serial.println("Generated labels:");
    for(auto label : labels) {
        Serial.printf("%s : %d\n", label.first.c_str(), label.second);
    }

    BMP::setAddress(CAN_ADDRESS);
    BMP::setCallback(MSG_TYPE::REGISTER, processREGISTER);
    BMP::setCallback(MSG_TYPE::STRIKE, processSTRIKE);
    BMP::setCallback(MSG_TYPE::DETONATE, processDETONATE);
    BMP::setCallback(MSG_TYPE::MARK_SOLVED, processMARK_SOLVED);
    BMP::setCallback(MSG_TYPE::CHANGE_TIMER, processCHANGE_TIMER);
    BMP::setCallback(MSG_TYPE::CHANGE_SERIAL_NO, processCHANGE_SERIAL_NO);
    BMP::setCallback(MSG_TYPE::TIMER, processTIMER);
    BMP::setCallback(MSG_TYPE::STRIKES, processSTRIKES);
    BMP::setCallback(MSG_TYPE::MODULE_COUNT, processMODULE_COUNT);
    BMP::setCallback(MSG_TYPE::ACTIVE_MODULE_COUNT, processACTIVE_MODULE_COUNT);
    BMP::setCallback(MSG_TYPE::LABELS, processLABELS);
    BMP::setCallback(MSG_TYPE::SERIAL_NO, processSERIAL_NO);
    BMP::setCallback(MSG_TYPE::DIFFICULTY, processDIFFICULTY);
    BMP::setCallback(MSG_TYPE::MAX_STRIKES, processMAX_STRIKES);
    BMP::setCallback(MSG_TYPE::RTFM, processRTFM);
    BMP::begin(1E6);

    for(int i = 1; i < 16; i++) {
        BMP::reqRTFM(i);
    }

    WiFi.mode(WIFI_AP);
    WiFi.softAP(wifiSSID);
    IPAddress IP = WiFi.softAPIP();
    Serial.print("AP IP address: ");
    Serial.println(IP);
    server.begin();
    server.setTimeout(3);
    addJob(millis(), listenWifi());
}
