#include <Arduino.h>

int getRounds();

int getRounds(){
    static int umdrehung = 0;
    bool pegel = false;

    // read the input on analog pin 0:
    int sensorValue = analogRead(OPTISCHER_SENSOR_PIN);
    // Convert the analog reading (which goes from 0 - 1023) to a voltage (0 - 5V):
    float voltage = sensorValue * (5.0 / 1023.0);
    if (voltage < 2 and pegel == 1)
        {
        umdrehung++;
        pegel = false;
        }

    if (voltage > 2 and pegel == false)
        {
        umdrehung++;
        pegel = true;
        }
    return umdrehung/2;
}
