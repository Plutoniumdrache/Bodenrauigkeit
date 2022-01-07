/*
* Diese Klasse bietet die Möglichkeit Zeiten zu messen.
* Die Methode setStartTime() setzt den Zeitpunkt ab wo
* die Zeit gemessen werden soll.
* Die Methode expiredTime() gibt zu dem Zeitpunkt, wo sie
* aufgerufen wird, die bereits vergangene Zeit zurück.
* Der Rückkgabewert ist in Millisekunden.
*/

#include <Arduino.h>

#define EXPIRED true
#define NOT_EXPIRED false
#define ACTIVATE true

class timer {
public:
timer();
virtual ~timer();
void setStartTime();
unsigned long expiredTime();
bool isTimeExpired(unsigned long milliseconds);
void resetTimer();
bool intervallTimer(unsigned long intervall);


private:
unsigned long startTime = 0;
unsigned long currentTime;

// reset timer
unsigned long tTime = 0;
bool entry = true;

// IntervallTimer
bool entry_intervall = true;
unsigned long tTime_intervall;
};