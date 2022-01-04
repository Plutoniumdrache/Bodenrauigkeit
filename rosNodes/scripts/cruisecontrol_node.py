#!/usr/bin/env python

import rospy
from std_msgs.msg import UInt16
from std_msgs.msg import Bool

startsignal = False

def callbackStartsignal(data):
    startsignal = data.data

def cruiseControl():
    # Subcribers
    subStartsignal = rospy.Subscriber('startsignal', Bool, callbackStartsignal)

    # Publishers
    pubSpeed = rospy.Publisher('speed', UInt16, queue_size=10)
    pubAngle = rospy.Publisher('angle', UInt16, queue_size=10)

    rospy.init_node('cruiseControl') # only one init call
    rate = rospy.Rate(1) # 1 Hz
    speed = 90
    angle = 90

    while not rospy.is_shutdown():
        rospy.loginfo("Speed: %s", str(speed))
        pubSpeed.publish(speed)

        rospy.loginfo("Angle: %s", str(angle))
        pubAngle.publish(angle)

        rate.sleep()

class CruiseControl:
    def __init__(self):
        # Parameter
        self.rate = rospy.Rate(1) # 1 Hz
        self.speed = 100
        self.angle = 93 # small offset correction because of the tape on the wheel
        self.startsignal = False
        self.rounds = 0

        # Subcribers
        self.subStartsignal = rospy.Subscriber('startsignal', Bool, self.callbackStartsignal)
        self.subRounds = rospy.Subscriber('rounds', UInt16, self.callbackRounds)

        # Publishers
        self.pubSpeed = rospy.Publisher('speed', UInt16, queue_size=10)
        self.pubAngle = rospy.Publisher('angle', UInt16, queue_size=10)

    
    def callbackStartsignal(self, data):
        self.startsignal = data.data
        self.speed = 85
        self.pubSpeedAngle()
    
    def callbackRounds(self, data):
        self.rounds = data.data
        if self.rounds >= 50:
            self.speed = 100
            self.pubSpeedAngle()
    
    def pubSpeedAngle(self):
        rospy.loginfo("Speed: %s", str(self.speed))
        self.pubSpeed.publish(self.speed)

        rospy.loginfo("Angle: %s", str(self.angle))
        self.pubAngle.publish(self.angle)
        

if __name__ == '__main__':
    rospy.init_node('cruiseControl') # only one init call
    CruiseControl()
    rospy.spin()
