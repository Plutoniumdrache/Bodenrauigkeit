#define USE_USBCON

#define SERVO_PIN 10
#define SPEED_PIN 6
#define LED_PIN 13
#include <Servo.h>
#include <ros.h>
#include <sensor_msgs/Joy.h>

#include <std_msgs/Int16MultiArray.h>

int l = 90;
int v = 90;
int Vneu = 90;
int Valt = 90;


Servo servo_lenkung;
Servo servo_fahrtenregler;

ros::NodeHandle nh;

void joy_cb(const std_msgs::Int16MultiArray& daten){
  
  
  l = daten.data[0];
  Vneu = daten.data[1];
  if (Vneu != Valt){
    servo_fahrtenregler.write(Vneu);
    Valt = Vneu;
  }
  
  servo_lenkung.write(l);
}

ros::Subscriber<std_msgs::Int16MultiArray> sub("/fahrwerte",joy_cb);

void setup(){
  nh.getHardware()->setBaud(9600);
  servo_lenkung.attach(SERVO_PIN);
  servo_fahrtenregler.attach(SPEED_PIN);
  nh.initNode();
  nh.subscribe(sub);
}

void loop(){
  nh.spinOnce();
  delay(125);
  if(v == 107){
    digitalWrite(LED_PIN, HIGH);
  }
  else {
    digitalWrite(LED_PIN, LOW);
  }
}
