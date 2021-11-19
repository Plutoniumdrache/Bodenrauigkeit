/*
 * rosserial Publisher Example
 * Prints "hello world!"


// Use the following line if you have a Leonardo or MKR1000
#define USE_USBCON

#include "Wire.h"
#include "I2Cdev.h"

#include <ros.h>
#include <std_msgs/String.h>
#include <std_msgs/Float32MultiArray.h>

ros::NodeHandle nh;

std_msgs::String str_msg;
std_msgs::Float32MultiArray arr;

ros::Publisher chatter("chatter", &str_msg);

char hello[13] = "hello world!";

void setup()
{
  nh.initNode();
  nh.advertise(chatter);
  arr.data_length = 9; // 9 Elemente
  arr.data = (float*)malloc(sizeof(float) * arr.data_length);
}

void loop()
{
  str_msg.data = hello;
  chatter.publish( &str_msg );
  nh.spinOnce();
  delay(1000);
} */