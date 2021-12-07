
#define USE_USBCON // because we are using an Arduino micro
 
#include <ros.h>
#include <std_msgs/Int16.h>
#include <std_msgs/Float32.h>
#include <std_msgs/Float32MultiArray.h>

#include "IMU.h" // functions for the IMU
#include "rounds.h"

// I2Cdev and MPU9250 must be installed as libraries, or else the .cpp/.h files
// for both classes must be in the include path of your project





ros::NodeHandle  nh;

// IMU Data
std_msgs::Float32MultiArray imu_msg;
ros::Publisher pub_imu("IMU", &imu_msg);

// Umdrehungs Data
std_msgs::Int16 rounds_msg;
ros::Publisher pub_rounds("rounds", &rounds_msg);

void setup() {
  // join I2C bus (I2Cdev library doesn't do this automatically)
  Wire.begin();

  nh.initNode();
  nh.advertise(pub_imu);
  nh.advertise(pub_rounds);

  imu_msg.data_length = 9; // 9 Elemente
  imu_msg.data = (float*)malloc(sizeof(float) * imu_msg.data_length);

  rounds_msg.data = 0;
}

void loop() 
{   

	// IMU:	
	getAccel_Data();
	getGyro_Data();
	getCompassDate_calibrated(); // compass data has been calibrated here 
	getHeading();				//before we use this function we should run 'getCompassDate_calibrated()' frist, so that we can get calibrated data ,then we can get correct angle .					
	getTiltHeading();           
	//delay(300); // ACHTUNG KANN PROBLEME MACHEN !!!

	// rounds:
	rounds_msg.data = getRounds();

    imu_msg.data[0] = Axyz[0];
    imu_msg.data[1] = Axyz[1];
    imu_msg.data[2] = Axyz[2];

    imu_msg.data[3] = Gxyz[0];
    imu_msg.data[4] = Gxyz[1];
    imu_msg.data[5] = Gxyz[2];

    imu_msg.data[6] = Mxyz[0];
    imu_msg.data[7] = Mxyz[1];
    imu_msg.data[8] = Mxyz[2];

    pub_imu.publish(&imu_msg);
	pub_rounds.publish(&rounds_msg);
    nh.spinOnce();
	
}
