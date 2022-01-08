#include <Arduino.h>

int getRounds(bool reset);

int getRounds(bool reset){
    static int umdrehung = 0;
    static bool pegel = false;
    if (reset){
        tmp = false;
        umdrehung = 0;
    }
    // read the input on analog pin 0:
    int sensorValue = analogRead(OPTISCHER_SENSOR_PIN);
    // Convert the analog reading (which goes from 0 - 1023) to a voltage (0 - 5V):
    float voltage = sensorValue * (5.0 / 1023.0);
    if (voltage < 2 and pegel == true){
            umdrehung++;
            pegel = false;
        }

    if (voltage > 2 and pegel == false){
            umdrehung++;
            pegel = true;
        }
    return umdrehung/2;
}
