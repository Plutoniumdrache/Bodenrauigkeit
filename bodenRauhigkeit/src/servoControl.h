#include <Arduino.h>
#include <Servo.h>

#include <ros.h>
#include <std_msgs/UInt16.h>

Servo lenkung;

void setLenkwinkel(const std_msgs::UInt16& cmd_msg){
  lenkung.write(cmd_msg.data); //set servo angle, should be from 0-180  
}

Servo ESC;

void setSpeed(const std_msgs::UInt16& cmd_msg){
  ESC.write(cmd_msg.data); //set speed and direction  
}