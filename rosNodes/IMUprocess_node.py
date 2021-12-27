#!/usr/bin/env python

from logging import FileHandler
import rospy
from std_msgs.msg import UInt16, Float32MultiArray, Bool
from datetime import date, datetime
from os.path import expanduser

# global_ax = 0
# global_ay = 0
# global_az = 0
# global_rotations = 0
# global_speed = 0
# global_startsignal = False
# flagFilename = False
# filename = ""
# fileHandle = None

# def callbackIMU(data):
#     global_ax = data.data[0]
#     global_ay = data.data[1]
#     global_az = data.data[2]
    
# def callbackRounds(data):
#     global_rotations = data.data

# def callbackSpeed(data):
#     global_speed = data.data

# def buildDataString(ax, ay, az, rotations, speed):
#     return str(ax + ',' + ay + ',' + az + ',' + rotations + ',' + speed + '\n')

# def callbackStartsignal(data):
#     global_startsignal = data.data

# def genFilename(flagFilename):
#     if flagFilename: 
#         dateTimeObj = datetime.now()
#         return dateTimeObj.strftime("%Y-%m-%d_%H-%M-%S")
    

# def writeToCSV (data, start):
#     pass
#     # file name generation
#     #if start:
        
#     #file = open(timestampStr, )
    

# def imuToCSV ():
#     rospy.init_node('imuToCSV')
#     rospy.Subscriber('IMU', Float32MultiArray, callbackIMU)
#     rospy.Subscriber('rounds', UInt16, callbackRounds)
#     rospy.Subscriber('speed', UInt16, callbackSpeed)
#     rospy.Subscriber('startsignal', Bool, callbackStartsignal)

#     if global_startsignal:
#         filename = genFilename(True)
#         fileHandle = open(filename, 'w')
#         global_ax = 0
#         global_ay = 0
#         global_az = 0
#         global_rotations = 0
#         global_speed = 0
#         global_startsignal = False
        
    
#     # check startbutton
#     # if startbutton
#         # generate filename
#         # 
#     # disable startbutton
#     # if rounds < 50
#         # write to csv
#     if global_rotations <= 50:
#         fileHandle.write(buildDataString(global_ax, global_ay, global_az, global_rotations, global_speed))
#     elif global_rotations > 50:
#         fileHandle.close()
#     rospy.spin()

class IMUProcess:
    def __init__(self):
        # Parameter
        self.global_ax = 0
        self.global_ay = 0
        self.global_az = 0
        self.global_rotations = 0
        self.global_speed = 0
        self.global_startsignal = False
        self.filename = ""
        self.fileHandle = None
        self.home = expanduser("~")
        
        # Subscribers
        rospy.Subscriber('IMU', Float32MultiArray, self.callbackIMU)
        rospy.Subscriber('rounds', UInt16, self.callbackRounds)
        rospy.Subscriber('speed', UInt16, self.callbackSpeed)
        rospy.Subscriber('startsignal', Bool, self.callbackStartsignal)

        # Publishers
            # none

    def imuToCsv(self):
        self.fileHandle = open(self.genFilename() + '.csv', 'w')
        self.fileHandle.write(self.buildDataString(self.global_ax, self.global_ay, self.global_az, self.global_rotations, self.global_speed))
        rospy.loginfo(self.buildDataString(self.global_ax, self.global_ay, self.global_az, self.global_rotations, self.global_speed))
        # if self.global_startsignal:
        #     self.filename = self.genFilename(True)
        #     #self.fileHandle = open(str(self.home + self.filename + '.csv'), 'w')
        #     self.fileHandle = open('x.csv', 'w')
        #     self.global_ax = 0
        #     self.global_ay = 0
        #     self.global_az = 0
        #     self.global_rotations = 0
        #     self.global_speed = 0
        #     self.global_startsignal = False
        
        # if self.global_rotations <= 50:
        #     #self.fileHandle.write(self.buildDataString(self.global_ax, self.global_ay, self.global_az, self.global_rotations, self.global_speed))
        #     rospy.loginfo(self.buildDataString(self.global_ax, self.global_ay, self.global_az, self.global_rotations, self.global_speed))
        # elif self.global_rotations > 50:
        #     self.fileHandle.close()
        

    def callbackIMU(self, data):
        self.global_ax = data.data[0]
        self.global_ay = data.data[1]
        self.global_az = data.data[2]
    
    def callbackRounds(self, data):
        self.global_rotations = data.data

    def callbackSpeed(self, data):
        self.global_speed = data.data

    def buildDataString(self, ax, ay, az, rotations, speed):
        return str(ax) + ',' + str(ay) + ',' + str(az) + ',' + str(rotations) + ',' + str(speed) + '\n'

    def callbackStartsignal(self, data):
        self.global_startsignal = data.data

    def genFilename(self):
        dateTimeObj = datetime.now()
        return dateTimeObj.strftime("%Y-%m-%d_%H-%M-%S")

if __name__ == '__main__':
    rospy.init_node('processIMU')
    node = IMUProcess()
    node.imuToCsv()
    rospy.spin()