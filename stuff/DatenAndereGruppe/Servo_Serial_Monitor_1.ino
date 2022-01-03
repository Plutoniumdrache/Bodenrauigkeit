
// Eingabe Informationen:
// Lenkung:       
//                links   grade   rechts
//                66      90      124
// Fahrtenregler: 
//    Vorwärts:   langsam   stop  schnell               
//                98        90    180
//    Rückwärts:  langsam   stop  schnell
//                80        90    0
//    Reset für Rückwärts: 2x 90

// Kommentare:
// Die Eingabe ist eine 7 stellige Zahl im Format 9vvvlll (bsp. 9100090)
// Die erste Ziffer ist eine Check Number

#define SERVO_PIN 10
#define SPEED_PIN 11
#include <Servo.h>

Servo servo_lenkung;
Servo servo_fahrtenregler;

//Globale Variablen
long   v   = 0;
long   l   = 0;
long   jp  = 0;


void setup()
{
  Serial.begin(9600);
  Serial.setTimeout(10); //Sorgt für ein schnelles Einlesen beim benutzen von Serial.parseInt();
  servo_lenkung.attach(SERVO_PIN);
  servo_fahrtenregler.attach(SPEED_PIN);
}


void ReadEingabe(){
    while(Serial.available() == 0)
    {}
    jp = Serial.parseInt();
    v  = long((jp - 9000000) / 1000);
    l  = jp - 9000000 - v*1000;
    if((v > 180)||(v < 0)){
      v = 90;  
      Serial.println("Fail Test v");
    }
    if((l > 124)||(l < 66)){
      l = 90;
      Serial.println("Fail Test l");
    }
    Serial.print("Geschwindigkeit: ");  
    Serial.println(v);
    Serial.print("Lenkung: ");  
    Serial.println(l);

}


void loop()
{
  ReadEingabe();
  servo_fahrtenregler.write(v);
  servo_lenkung.write(l); 
  Serial.println(jp);
  //delay(100);
}
