
#define USE_USBCON // because we are using an Arduino micro
#define OPTISCHER_SENSOR_PIN A5
#define LENKUNG_PWM_PIN 9
#define ESC_PWM_PIN 13

#include <ros.h>
#include <std_msgs/Int16.h>
#include <std_msgs/Float32.h>
#include <std_msgs/Float32MultiArray.h>

#include "IMU.h" // functions for the IMU
#include "rounds.h"


void getIMUdata(void);


ros::NodeHandle  nh;

// Umdrehungs Data
std_msgs::Int16 rounds_msg;
ros::Publisher pub_rounds("rounds", &rounds_msg);

// IMU Data
std_msgs::Float32MultiArray imu_msg;
ros::Publisher pub_imu("IMU", &imu_msg);




void setup() {
  // join I2C bus (I2Cdev library doesn't do this automatically)
  Wire.begin();

  nh.advertise(pub_imu);
  nh.advertise(pub_rounds);

  rounds_msg.data = 0;

  imu_msg.data_length = 9; // 9 Elemente
  imu_msg.data = (float*)malloc(sizeof(float) * imu_msg.data_length);
}

void loop() 
{   
	// IMU:	
	getAccel_Data();
	getGyro_Data();
	getCompassDate_calibrated(); // compass data has been calibrated here 
	getHeading();				//before we use this function we should run 'getCompassDate_calibrated()' frist, so that we can get calibrated data ,then we can get correct angle .					
	getTiltHeading();

	rounds_msg.data = getRounds();
	getIMUdata();
	pub_rounds.publish(&rounds_msg);
    pub_imu.publish(&imu_msg);

	nh.spinOnce();
	delay(300);
}

void getIMUdata(void){
	
	imu_msg.data[0] = Axyz[0];
	imu_msg.data[1] = Axyz[1];
	imu_msg.data[2] = Axyz[2];

	imu_msg.data[3] = Gxyz[0];
	imu_msg.data[4] = Gxyz[1];
	imu_msg.data[5] = Gxyz[2];
	
	imu_msg.data[6] = Mxyz[0];
	imu_msg.data[7] = Mxyz[1];
	imu_msg.data[8] = Mxyz[2];
}