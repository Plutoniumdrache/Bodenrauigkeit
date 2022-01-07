#include "timer.h"

timer::timer() {

}

/* Setzen der Startzeit, ab hier wird die Zeit gemessen */
void timer::setStartTime() {
    startTime = millis(); 
}

/*
* Berechnung der vergangenen Zeit vom setzen der Startzeit
* mit setStartTime() an, bis zum Zeitpubkt an der die Methode
* expiredTime() aufgerufen wird.
* Rückgabe der vergangenen Zeit in Millisekunden.
*/
unsigned long timer::expiredTime() {
    currentTime = millis();
    return (currentTime - startTime);
}

/* 
* Die Methode gibt zuruück ob die angebene Zeit in Millisekunden 
* abgelaufen ist.
* Rückgabewert:
* - true: Zeit ist abgelaufen
* - false: Zeit ist nicht abgelaufen 
* ACHTUNG: Timer muss zurückgesetzt werden
*/
bool timer::isTimeExpired(unsigned long milliseconds) {
    // entry marker, da die Startzeit gemerkt werden muss
    if(entry)
    {
        tTime = millis();
        entry = false;
    }
    unsigned long actualTime = millis();
    // Berechnung der bereits vergangenen Zeit:
    if( (actualTime - tTime) >= milliseconds)
    {
        return EXPIRED; // Zeit abgelaufen
    } else
    {
        return NOT_EXPIRED; // Zeit nicht abgelaufen
    }
}

/* Zurücksetzen des Timers der Methode isTimeExpired */
void timer::resetTimer()
{
    entry = ACTIVATE;
}

/*  liefert in Abständen des angebenen Zeitintervalls true, 
    reset passiert automatisch nach Ablauf der Zeit */
bool timer::intervallTimer(unsigned long intervall)
{
        // entry marker, da die Startzeit gemerkt werden muss
    if(entry_intervall)
    {
        tTime_intervall = millis();
        entry_intervall = false;
    }
    unsigned long actualTime = millis();
    // Berechnung der bereits vergangenen Zeit:
    if( (actualTime - tTime_intervall) >= intervall)
    {
        entry_intervall = true; // entry marker für das setzen der Startzeit zurücksetzen
        return EXPIRED; // Zeit abgelaufen
    } else
    {
        return NOT_EXPIRED; // Zeit nicht abgelaufen
    }
}

timer::~timer() {

}