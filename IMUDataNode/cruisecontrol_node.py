#!/usr/bin/env python

import rospy
from std_msgs.msg import UInt16

def Fahrverhalten():
    pubSpeed = rospy.Publisher('speed', UInt16, queue_size=10)
    pubAngle = rospy.Publisher('angle', UInt16, queue_size=10)
    rospy.init_node('speed')
    rospy.init_node('angle')
    rate = rospy.Rate(10)
    speed = 90
    angle = 90
    while not rospy.is_shutdown():
        rospy.loginfo(speed)
        rospy.loginfo(angle)
        pubSpeed.publish(speed)
        pubSpeed.publish(angle)
        rate.sleep


if __name__ == '__main__':
    try:
        Fahrverhalten()
    except rospy.ROSInterruptException: # because we using sleep
        pass