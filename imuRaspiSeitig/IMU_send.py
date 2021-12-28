# MPU6050 9-DoF Example Printout

from mpu9250_i2c import *
import rospy
import std_msgs


time.sleep(1) # delay necessary to allow mpu9250 to settle

def collectData():
    while 1:
        try:
            ax,ay,az,wx,wy,wz = mpu6050_conv() # read and convert mpu6050 data
        except:
            continue
        accela = [2]
        accela[0] = ax
        accela[1] = ay
        accela[2] = az

        pubAccel = rospy.Publisher('accel', tupel)
        rospy.init_node('accel')
        rate = rospy.Rate(10)
        
        while not rospy.is_shutdown():
            rospy.loginfo(speed)
            rospy.publish(accel)
            rate.sleep

if __name__ == '__main__':
    try:
        collectData()
    except rospy.ROSInterruptException:
        pass

