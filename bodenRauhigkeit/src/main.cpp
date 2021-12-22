
#define USE_USBCON // because we are using an Arduino micro
#define OPTISCHER_SENSOR_PIN A5
#define LENKUNG_PWM_PIN 9
#define ESC_PWM_PIN 13
#define STARTSIGNAL_PIN 2

#include <ros.h>
#include <std_msgs/Int16.h>
#include <std_msgs/Float32.h>
#include <std_msgs/Bool.h>

#include "rounds.h"
#include "button.h"

ros::NodeHandle  nh;

// Umdrehungs Data:
std_msgs::Int16 rounds_msg;
ros::Publisher pub_rounds("rounds", &rounds_msg);

// Startsignal:
std_msgs::Bool startsignal_msg;
ros::Publisher pub_startsignal("startsignal", &startsignal_msg);





void setup() {
 
  nh.advertise(pub_rounds);
  nh.advertise(pub_startsignal);


  rounds_msg.data = 0;
  startsignal_msg.data = true;

  // Tasterstuff:
  pinMode(STARTSIGNAL_PIN, INPUT_PULLUP);

}

void loop() 
{   

	rounds_msg.data = getRounds();
	startsignal_msg.data = getButtonState(STARTSIGNAL_PIN);
	
	pub_rounds.publish(&rounds_msg);
	pub_startsignal.publish(&startsignal_msg);

	nh.spinOnce();
	delay(300);
}
