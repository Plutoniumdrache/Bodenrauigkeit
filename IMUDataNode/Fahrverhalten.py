import rospy
import std_msgs

def Fahrverhalten():
    pubSpeed = rospy.Publisher('speed', int)
    pubAngle = rospy.Publisher('angle', int)
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
    except rospy.ROSInterruptException:
        pass