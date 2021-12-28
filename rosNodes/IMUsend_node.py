#!/usr/bin/env python
"""
ROS node for collecting and sending the data from the IMU on the topic IMU
"""

from mpu9250_i2c import *
import rospy
from std_msgs.msg import Float32MultiArray

# sleep in here not good
time.sleep(1) # delay necessary to allow mpu9250 to settle

def collectData():
    pub = rospy.Publisher('IMU', Float32MultiArray, queue_size=10)
    rospy.init_node('IMU')
    rate = rospy.Rate(10)
    accelData = Float32MultiArray()
        
    while not rospy.is_shutdown():
        try:
            ax,ay,az,wx,wy,wz = mpu6050_conv() # read and convert mpu6050 data
        except:
            continue
        
        accelData = [ax, ay, az]
        
        rospy.loginfo("accelData: ", str(accelData[0] + accelData[1] + accelData[2]))
        pub.publish(accelData)
        rate.sleep

if __name__ == '__main__':
    try:
        collectData()
    except rospy.ROSInterruptException:
        pass

