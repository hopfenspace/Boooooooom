#include <map>
#include <string>
#include <vector>
#include <functional>
#include <tuple>
#include <stdlib.h>

#include <Arduino.h>
#include <CAN.h>

#include "wordlist.h"

#define MORSE_LED 17
#define STRIKE_LED 18
#define SOLVED_LED 19

#define LEFT_BUTTON 15
#define RIGHT_BUTTON 16
#define SUBMIT_BUTTON 2

#define CAN_RX 4
#define CAN_TX 5


enum difficulty{EASY=320, NORMAL=160, HARD=80, EXPERT=40, PREPARE_2_DIE=20};

std::map<char, std::string> morseCode = {
    {'a', ".-"}, {'b', "-..."}, {'c', "-.-."}, {'d', "-.."}, {'e', "."}, {'f', "..-."}, {'g', "--."}, 
    {'h', "...."}, {'i', ".."}, {'j', ".---"}, {'k', "-.-"}, {'l', ".-.."}, {'m', "--"}, {'n', "-."},
    {'o', "---"}, {'p', ".--."}, {'q', "--.-"}, {'r', ".-."}, {'s', "..."}, {'t', "-"}, {'u', "..-"},
    {'v', "...-"}, {'w', ".--"}, {'x', "-..-"}, {'y', "-.--"}, {'z', "--.."}, {'1', ".----"}, 
    {'2', "..---"}, {'3', "...--"}, {'4', "....-"}, {'5', "....."}, {'6', "-...."}, {'7', "--..."}, 
    {'8', "---.."}, {'9', "----."}, {'0', "-----"}, {' ', "/"}
};

int unitTime;
boolean solved;
std::string chosenOne;
std::string current;
std::vector<std::string> wordlist;
std::vector<int> frequencies;
std::map<std::string, int> wordlistLookup;

int jobCounter = 0;
std::vector<std::tuple<int, int, std::function<void()>>> jobs;


void addJob(unsigned long execution_time, std::function<void()> callback) {
    jobs.push_back(std::make_tuple(jobCounter, execution_time, callback));
    jobCounter++;
}

std::function<void()> turnLEDOn(int nextExecutionDelta);
std::function<void()> turnLEDOn(int nextExecutionDelta) {
    return [nextExecutionDelta]() {
        digitalWrite(MORSE_LED, 1);
        addJob(millis() + nextExecutionDelta, turnLEDOn(nextExecutionDelta));
    };
}

std::function<void()> turnLEDOff(int nextExecutionDelta);
std::function<void()> turnLEDOff(int nextExecutionDelta) {
    return [nextExecutionDelta](){
        digitalWrite(MORSE_LED, 0);
        addJob(millis() + nextExecutionDelta, turnLEDOff(nextExecutionDelta));
    };
}

std::vector<std::string> translate_to_morse(std::string sentence, boolean end_with_pause = true) {
    std::vector<std::string> translated;

    for(int i = 0; i < sentence.length(); i++) {
        sentence[i] = tolower(sentence[i]);
        translated.push_back(morseCode[sentence[i]]);
    }
    if (end_with_pause && translated[translated.size()-1] != "/") {
        translated.push_back("/");
    }
    return translated;
}

void write_morse(std::string sentence) {
    std::vector<std::string> translated = translate_to_morse(sentence);

    int unitCounter = 0;
    for(int i = 0; i < translated.size(); i++) {
        for(int j = 0; j < translated[i].size(); j++) {
            if(translated[i][j] == '.') {
                // Dot is 1 unit
                unitCounter++;
            } else if(translated[i][j] == '-') {
                // Dash is 3 units
                unitCounter += 3;
            } else if(translated[i][j] == '/') {
                // Word pause is 7 units
                unitCounter += 7;
            }
            if(j != translated[i].size() - 1) {
                // Intra character pause is 1 unit
                unitCounter++;
            } else {
                if(translated[i][j] != '/' && i != translated.size()-1 && translated[i+1] != "/") {
                    // Current char is no word pause and next char is no word pause
                    // Inter character pause is 3 units
                    unitCounter += 3;
                }
            }
        }
    }

    int nextExecutionDelta = unitTime * unitCounter;

    int counter = 0;
    for(int i = 0; i < translated.size(); i++) {
        for(int j = 0; j < translated[i].size(); j++) {
            if(translated[i][j] == '.') {
                addJob(millis() + counter*unitTime, turnLEDOn(nextExecutionDelta));
                counter++;
            } else if(translated[i][j] == '-') {
                addJob(millis() + counter*unitTime, turnLEDOn(nextExecutionDelta));
                counter += 3;
            } else if(translated[i][j] == '/') {
                addJob(millis() + counter*unitTime, turnLEDOff(nextExecutionDelta));
                counter += 7;
            }
            if(j != translated[i].size()-1) {
                // Intra character pause
                addJob(millis() + counter*unitTime, turnLEDOff(nextExecutionDelta));
                counter++;
            } else {
                if(translated[i][j] != '/' && i != translated.size()-1 && translated[i+1] != "/") {
                    // Inter character pause
                    addJob(millis() + counter*unitTime, turnLEDOff(nextExecutionDelta));
                    counter += 3;
                }
            }
        }
    }
}

void handleLeft() {
    int index = 0;
    for (int i = 0; i < wordlist.size(); i++) {
        if (current == wordlist[i]) {
            index = i;
            break;
        }
    }
    if (index > 0) {
        current = wordlist[index-1];
    }
    Serial.printf("Current word: %s\n", current.c_str());
}

void irqLeft() {
    addJob(millis(), handleLeft);
}

void handleRight() {
    int index = 0;
    for (int i = 0; i < wordlist.size(); i++) {
        if(current == wordlist[i]) {
            index = i;
            break;
        }
    }
    if(index != wordlist.size()-1) {
        current = wordlist[index+1];
    }
    Serial.printf("Current word: %s\n", current.c_str());
}

void irqRight() {
    addJob(millis(), handleRight);
}

void irqSubmit() {
    if (current == chosenOne) {
        solved = true;
    } else {
        // TODO: Push job: send strike
        addJob(millis(), [](){
            digitalWrite(STRIKE_LED, 1);
        });
        addJob(millis()+300, []() {
            digitalWrite(STRIKE_LED, 0);
        });
    }
}

void loop() {
    if (solved) {
        digitalWrite(SOLVED_LED, 1);
        return;
    }

    // Process jobs
    std::vector<int> eraseList;
    for(int i = 0; i < jobs.size(); i++) {
        if(std::get<1>(jobs[i]) <= millis()) {
            std::get<2>(jobs[i])();
            eraseList.push_back(std::get<0>(jobs[i]));
        }
    }
    // Delete elements from jobs that are already executed
    for(int i = 0; i < eraseList.size(); i++) {
        int index = 0;
        for (int x = 0; x < jobs.size(); x++) {
            if(std::get<0>(jobs[x]) == eraseList[i]) {
                index = x;
                break;
            }
        }
        jobs.erase(jobs.begin() + index);
    }
}

void setup_game(difficulty difficulty, int possibleWordCount) {
    attachInterrupt(digitalPinToInterrupt(LEFT_BUTTON), irqLeft, RISING);
    attachInterrupt(digitalPinToInterrupt(RIGHT_BUTTON), irqRight, RISING);
    attachInterrupt(digitalPinToInterrupt(SUBMIT_BUTTON), irqSubmit, RISING);

    unitTime = difficulty;
    if (difficulty >= 160) {
        std::vector<std::string> words5;
        for(auto word: availableWords) {
            if (word.length() == 5) {
                words5.push_back(word);
            }
        }
        int start = words5.size() - rand() % words5.size() - possibleWordCount;
        for(int i = start; i < start + possibleWordCount; i++) {
            wordlist.push_back(words5[i]);
        }
    } else {
        int start = availableWords.size() - rand() % availableWords.size() - possibleWordCount;
        for(int i = start; i < start + possibleWordCount; i++) {
            wordlist.push_back(availableWords[i]);
        }
    }

    while(frequencies.size() != possibleWordCount) {
        frequencies.push_back(rand() % 9000 + 1000);
    }

    std::sort(wordlist.begin(), wordlist.end());
    std::sort(frequencies.begin(), frequencies.end());

    for(int i = 0; i < possibleWordCount; i++) {
        wordlistLookup.insert(std::pair<std::string, int>(wordlist[i], frequencies[i]));
    }

    current = wordlist[rand() % wordlist.size()];
    chosenOne = wordlist[rand() % wordlist.size()];

    for(int i = 0; i < possibleWordCount; i++) {
        Serial.printf("Word: %s; Frequency: %d\n", wordlist[i].c_str(), frequencies[i]);
    }

    Serial.printf("Chosen Word: %s, its frequency: %d\n", chosenOne.c_str(), wordlistLookup[chosenOne]);
}

void setup() {
    Serial.begin(115200);

    pinMode(MORSE_LED, OUTPUT);
    pinMode(STRIKE_LED, OUTPUT);
    pinMode(SOLVED_LED, OUTPUT);

    pinMode(LEFT_BUTTON, INPUT);
    pinMode(RIGHT_BUTTON, INPUT);
    pinMode(SUBMIT_BUTTON, INPUT);

    Serial.println("Setting up CAN");
    CAN.setPins(CAN_RX, CAN_TX);
    while(!CAN.begin(1E6)) {
        Serial.println("CAN startup failed, retrying in 1 second");
        delay(1000);
    }
    Serial.println("CAN set up successfully");

    Serial.println("Changing seed of srand");
    srand(esp_random());

    Serial.println("Initialization complete");

    Serial.println("Setting up game");
    setup_game(NORMAL, 16);

    solved = false;
    Serial.println("Game is ready");

    Serial.println("Starting Game");
    write_morse(chosenOne);
}
