import rospy
import std_msgs
from datetime import date, datetime

global_ax = 0
global_ay = 0
global_az = 0
global_rotations = 0
global_speed = 0
global_startsignal = False
flagFilename = False
filename = ""
fileHandle = None

def callbackIMU(data):
    global_ax = data.data[0]
    global_ay = data.data[1]
    global_az = data.data[2]
    
def callbackRounds(data):
    global_rotations = data.data

def callbackSpeed(data):
    global_speed = data.data

def buildDataString(ax, ay, az, rotations, speed):
    return str(ax + ',' + ay + ',' + az + ',' + rotations + ',' + speed + '\n')

def callbackStartsignal(data):
    global_startsignal = data.data

def genFilename(flagFilename):
    if flagFilename: 
        dateTimeObj = datetime.now()
        return dateTimeObj.strftime("%Y-%m-%d_%H-%M-%S")
    

def writeToCSV (data, start):
    pass
    # file name generation
    #if start:
        
    #file = open(timestampStr, )
    

def imuToCSV ():
    rospy.init_node('imuToCSV')
    rospy.Subscriber('IMU', tuple, callbackIMU)
    rospy.Subscriber('rounds', int, callbackRounds)
    rospy.Subscriber('speed', int, callbackSpeed)
    rospy.Subscriber('startsignal', bool, callbackStartsignal)

    if global_startsignal:
        filename = genFilename(True)
        fileHandle = open(filename, 'w')
        global_ax = 0
        global_ay = 0
        global_az = 0
        global_rotations = 0
        global_speed = 0
        global_startsignal = False
        
    
    # check startbutton
    # if startbutton
        # generate filename
        # 
    # disable startbutton
    # if rounds < 50
        # write to csv
    if global_rotations <= 50:
        fileHandle.write(buildDataString(global_ax, global_ay, global_az, global_rotations, global_speed))
    elif global_rotations > 50:
        fileHandle.close()
    rospy.spin()

if __name__ == '__main__':
    imuToCSV()