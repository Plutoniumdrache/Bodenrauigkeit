#include "Arduino.h"

bool getButtonState(int pinNumber){
    return !digitalRead(pinNumber);
}