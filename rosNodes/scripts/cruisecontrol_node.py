#!/usr/bin/env python

"""
ROS node for controlling the RC-Car and driving a specific distance
"""

import rospy
from std_msgs.msg import UInt16
from std_msgs.msg import Bool

class CruiseControl:
    def __init__(self):
        # Parameter
        self.rate = rospy.Rate(1) # 1 Hz
        self.vehicleStop = 90 # vehicle stops
        self.speed = 90 # init with vehicle stop value
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
        self.speed = 85 # slow forward
        self.pubSpeedAngle()
    
    def callbackRounds(self, data):
        self.rounds = data.data
        if self.rounds >= 45:
            self.speed = self.vehicleStop
            self.pubSpeedAngle()
    
    def pubSpeedAngle(self):
        rospy.loginfo("Speed: %s", str(self.speed))
        self.pubSpeed.publish(self.speed)

        rospy.loginfo("Angle: %s", str(self.angle))
        self.pubAngle.publish(self.angle)
        

if __name__ == '__main__':
    rospy.init_node('cruiseControl') # only one init call
    rospy.loginfo("started cruisecontrol node")
    CruiseControl()
    rospy.spin()
