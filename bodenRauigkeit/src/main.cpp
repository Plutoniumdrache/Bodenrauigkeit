
#define USE_USBCON // because we are using an Arduino micro
#define OPTISCHER_SENSOR_PIN A5
#define LENKUNG_PWM_PIN 9
#define ESC_PWM_PIN 13
#define STARTSIGNAL_PIN 2

// globals
int speed = 0;
bool tmp = false;

#include <ros.h>
#include <std_msgs/UInt16.h>
#include <std_msgs/Float32.h>
#include <std_msgs/Bool.h>

#include "rounds.h"
#include "button.h"
#include "servoControl.h"
#include "timer.h"


ros::NodeHandle  nh;
timer clock;
button startbutton;

// Umdrehungs Data:
std_msgs::UInt16 rounds_msg;
ros::Publisher pub_rounds("rounds", &rounds_msg);

// Startsignal:
std_msgs::Bool startsignal_msg;
ros::Publisher pub_startsignal("startsignal", &startsignal_msg);

// Lenkungs Servo PWM
ros::Subscriber<std_msgs::UInt16> sub_lenkung("angle", setLenkwinkel);

// ESC PWM
ros::Subscriber<std_msgs::UInt16> sub_speed("speed", setSpeed);


void setup() {
  startbutton.initializeButton(STARTSIGNAL_PIN);

  nh.advertise(pub_rounds);
  nh.advertise(pub_startsignal);

  rounds_msg.data = 0;
  startsignal_msg.data = true;

  nh.subscribe(sub_lenkung);
  lenkung.attach(LENKUNG_PWM_PIN);

  nh.subscribe(sub_speed);
  ESC.attach(ESC_PWM_PIN);
}

void loop() 
{   
	startsignal_msg.data = startbutton.isButtonPressed();
  if(startsignal_msg.data){
    pub_startsignal.publish(&startsignal_msg);
    tmp = true;
  }

  rounds_msg.data = getRounds(tmp);
  pub_rounds.publish(&rounds_msg);

	nh.spinOnce();
  delay(30);
}
