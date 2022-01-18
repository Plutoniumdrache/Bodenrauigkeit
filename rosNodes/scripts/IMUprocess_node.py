#!/usr/bin/env python

"""
ROS node for logging the data from the IMU, the number of rotations and 
the speed PWM signal value. The data is being stored in a .csv file on an USB flash drive.
"""

import rospy
from std_msgs.msg import UInt16, Float32MultiArray, Bool, String
from datetime import date, datetime

class IMUProcess:
    def __init__(self):
        # Parameter
        self.ax = 0
        self.ay = 0
        self.az = 0
        self.rotations = 0
        self.speed = 0
        self.startsignal = False
        self.filename = ''
        self.fileHandle = None
        self.running = False
        self.maxRotations = 10
        
        # Subscribers
        rospy.Subscriber('IMU', Float32MultiArray, self.callbackIMU)
        rospy.Subscriber('rounds', UInt16, self.callbackRounds)
        rospy.Subscriber('speed', UInt16, self.callbackSpeed)
        rospy.Subscriber('startsignal', Bool, self.callbackStartsignal)
        rospy.Subscriber('drivedistance', UInt16, self.callbackDriveDistance)

        # Publishers
        self.pubFilepath = rospy.Publisher('filepath', String, queue_size=1)
        
    def callbackIMU(self, data):
        rospy.loginfo("startsignal in imuToCsv: %s", str(self.startsignal))
        if self.startsignal:
            # because were using the autofs function to automount the flash drive the path is /automnt/usb-stick/
            self.filename = self.genFilename()
            self.fileHandle = open('/automnt/usb-stick/' + self.filename + '.csv', 'w')
            self.ax = 0
            self.ay = 0
            self.az = 0
            self.rotations = 0
            self.startsignal = False
            self.running = True
            rospy.loginfo("got the f****** signal")
        
        self.ax = data.data[0]
        self.ay = data.data[1]
        self.az = data.data[2]
        
        if self.running:
            if self.rotations <= self.maxRotations:
                self.fileHandle.write(self.buildDataString(self.ax, self.ay, self.az, self.rotations, self.speed))
                rospy.loginfo(self.buildDataString(self.ax, self.ay, self.az, self.rotations, self.speed))
            if self.rotations >= self.maxRotations:
                self.fileHandle.close()
                self.running = False
                self.pubFilepath.publish(self.filename)

    def callbackRounds(self, data):
        self.rotations = data.data

    def callbackSpeed(self, data):
        self.speed = data.data

    def buildDataString(self, ax, ay, az, rotations, speed):
        return str(ax) + ',' + str(ay) + ',' + str(az) + ',' + str(rotations) + ',' + str(speed) + '\n'

    def callbackStartsignal(self, data):
        self.startsignal = data.data
        rospy.loginfo("current startsignal is: %s", str(data.data))
    
    def callbackDriveDistance(self, data):
        self.maxRotations = data.data

    def genFilename(self):
        dateTimeObj = datetime.now()
        return dateTimeObj.strftime("%Y-%m-%d_%H-%M-%S")

if __name__ == '__main__':
    rospy.init_node('processIMU')
    rospy.loginfo("started IMUprocess node")
    IMUProcess()
    rospy.spin()