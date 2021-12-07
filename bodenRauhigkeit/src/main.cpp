
#define USE_USBCON // because we are using an Arduino micro
#define OPTISCHER_SENSOR_PIN A5
#define LENKUNG_PWM_PIN 9
#define ESC_PWM_PIN 13

#include <ros.h>
#include <std_msgs/Int16.h>

#include "rounds.h"


ros::NodeHandle  nh;

// Umdrehungs Data
std_msgs::Int16 rounds_msg;
ros::Publisher pub_rounds("rounds", &rounds_msg);


void setup() {
  
  nh.advertise(pub_rounds);

  rounds_msg.data = 0;
}

void loop() 
{   
	rounds_msg.data = getRounds();
	pub_rounds.publish(&rounds_msg);
    nh.spinOnce();
	delay(300);
}
