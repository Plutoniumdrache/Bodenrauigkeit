#!/usr/bin/env python
# coding: utf-8
"""
ROS node for evaluating the IMU accelaration data.
Author: Jakob Rohwer
Editor: Julius Preuschoff
"""


import numpy as np
import rospy
from std_msgs.msg import String
import os

class IMUeval:
    def __init__(self):
        # Const Variables:
        self.rotationDistance = 0.18 # meter
        self.sigma = 2.2 # calculate borders with 3 sigma rule (2.2 sigma is used because of few data)
        self.filepath = '/automnt/usb-stick/'

        # Parameters
        self.raw_data = None
        self.filename = ''
        self.vek_driveDistance = None
        self.data = None
        self.z_accel_clean = None
        self.z_accel_clean_woPeaks = None
        self.root_z_ges = None
        self.roughness = 0
        self.root_vek_z = None
        self.speed = 0
        self.filehandle = None
        self.doorstepNum = []
        self.doorstepPos = []

        # Subscribers
        rospy.Subscriber('filepath', String, self.callbackFilepath)

        # Publishers
            # none

    def getRawData(self, filepath):
        # path for tests
        # path = os.path.dirname(os.path.abspath(__file__))
        # fullpath = str(path + '/' + self.filename)
        self.raw_data = np.genfromtxt(filepath, delimiter=',')

    def calcDriveDistance(self):
        # ueberfluessige Werte abschneiden
        for i in range(0, len(self.raw_data)):
            if self.raw_data[i][3] < self.raw_data[i-1][3]:
                rotations = self.raw_data[i-1][3]
                rotations_i = i - 1
                break        
        self.data = self.raw_data[:rotations_i]

        # calculate driveDistance from rotations
        driveDistance = self.rotationDistance * rotations
        self.vek_driveDistance = np.linspace(0, driveDistance, len(self.data))
    
    def cleanData(self):
        # offset der z-Beschl.werte entfernen
        z_mean = np.mean(self.data[:,2])
        self.z_accel_clean = self.data[:,2] - z_mean

        # Ausreißer entfernen        
        negativeBorder = np.mean(self.z_accel_clean) - self.sigma * np.std(self.z_accel_clean)
        positiveBorder = np.mean(self.z_accel_clean) + self.sigma * np.std(self.z_accel_clean)
        
        # delete Data out of borders 
        lower = np.where(self.z_accel_clean < negativeBorder)
        self.z_accel_clean_woPeaks = np.delete(self.z_accel_clean,lower)
        higher = np.where(self.z_accel_clean_woPeaks > positiveBorder)
        self.z_accel_clean_woPeaks = np.delete(self.z_accel_clean_woPeaks,higher)

    def RMS_Z(self):
        #RMS ueber alle Werte nur fuer z
        n1 = len(self.z_accel_clean_woPeaks) #Bereich festlegen
        j = 0

        while j < len(self.z_accel_clean_woPeaks) - n1 + 1:   
            square_z = 0  
            for i in range(0,n1):
                square_z += (self.z_accel_clean_woPeaks[j+i]**2)   
            mean_z = square_z / n1
            root_z = np.sqrt(mean_z)    
            j += i + 1

        self.root_z_ges = root_z
    def classification(self):
        """Klassifikator Versuch 2 Fuer alle V"""

        self.speed = self.raw_data[0][4] # ACHTUNG HIER MUSS IMMER DIE AKTUELLE GESCHWINDIGKEIT STEHEN
        # EVT AUS CSV EINLESEN
        # Grenzwerte
        threshhold_85 = np.linspace(0,0.745,101)
        threshhold_84 = threshhold_85 * 1.328770712165726
        threshhold_83 = threshhold_84 * 1.040784135069001
        # Rauigkeit bestimmen
        if(self.speed == 85):
            for i in range(0,len(threshhold_85)):
                if(self.root_z_ges <= threshhold_85[i]):
                    self.roughness = i
                    break
            if(self.root_z_ges > threshhold_85[100]):
                self.roughness = 100
        elif(self.speed == 84):
            for i in range(0,len(threshhold_84)):
                if(self.root_z_ges <= threshhold_84[i]):
                    self.roughness = i
                    break
            if(self.root_z_ges > threshhold_84[100]):
                self.roughness = 100 
        elif(self.speed == 83):
            for i in range(0,len(threshhold_83)):
                if(self.root_z_ges <= threshhold_83[i]):
                    self.roughness = i
                    break
            if(self.root_z_ges>threshhold_83[100]):
                self.roughness = 100

    def displayRoughness(self, filehandle):
        # Ausgabe der Rauigkeit und der Boden Vermutung
        filehandle.write('Die Rauigkeit des Bodens betraegt: ' + str(self.roughness) + ' %\n')
        if(self.roughness <= 26):
            filehandle.write('Das entspricht z.B. Laborboden\n')
        elif(self.roughness <= 31):
            filehandle.write('Das entspricht z.B. Asphalt\n')
        elif(self.roughness <= 41):
            filehandle.write('Das entspricht z.B. Pflastersteinen\n')
        else:
            filehandle.write('Das entspricht z.B. Kopfsteinpflaster\n')
    
    def callbackFilepath(self, data):
        self.filename = data.data
        path = str(self.filepath + self.filename + '.csv')
        
        # floor
        self.getRawData(path)
        self.calcDriveDistance()
        self.cleanData()
        self.RMS_Z()
        self.classification()
        
        # door steps
        self.doorSteps_RMS_Z()
        self.detectDoorSteps()
        self.genLogFile()

    def doorSteps_RMS_Z(self):
        """calc RMS for the doorstep detection"""
        #RMS ueber festgelegte Anzahl an Werten fuer z
        n = 3 #Bereich festlegen
        self.root_vek_z = []
        j = 0

        while j < len(self.z_accel_clean) - n + 1:
            square_z = 0    
            for i in range(0,n):
                square_z += (self.z_accel_clean[j+i]**2)
            mean_z = square_z/n
            root_z = np.sqrt(mean_z)    
            for i in range(0,n):
                self.root_vek_z.append(root_z)
            j += i + 1
        # Auffuellen der letzten Werte falls Gesamtanzahl nicht durch n Teilbar
        while len(self.z_accel_clean)-len(self.root_vek_z):
            self.root_vek_z.append(self.root_vek_z[len(self.root_vek_z)-1])
    
    def detectDoorSteps(self):
        """Bodenschwellen detektieren"""
        self.doorSteps_RMS_Z()

        border = 3 * np.mean(self.root_vek_z) 
        j = 0
        merker = 0

        for i in range(0,len(self.root_vek_z)):
            if self.root_vek_z[i] > border and merker == 0:  # vorher border
                if self.root_vek_z[i+1] <= border:
                    break
                if self.root_vek_z[i+2] <= border:
                    break
                #Anzahl der Tuerschwellen
                self.doorstepNum.append(j)
                #Position der Tuerschwellen
                self.doorstepPos.append(self.vek_driveDistance[i])
                j += 1
                merker = 1
            # verhindert das aufeinanderfolgende Werte mehrere Tuerschwellen triggern    
            if self.root_vek_z[i] <= border:
                merker = 0
    
    def displayDoorSteps(self, filehandle):
        """Ausgabe der Lage der Boden- bzw. Tuerschwellen"""        
        filehandle.write('Es gibt ' + str(len(self.doorstepNum)) + ' Tuerschwellen\n')
        if len(self.doorstepNum):
            for i in range(0,len(self.doorstepNum)):
                filehandle.write('Tuerschwelle ' + str(self.doorstepNum[i] + 1) + ' bei ' + str(round(self.doorstepPos[i],1)) + ' Metern\n')
        if len(self.doorstepNum) == 2:
            if self.speed == 85:
                self.roughness -= 5 # correct the roughness value
            elif self.speed == 84:
                self.roughness -= 10 # correct the roughness value
        if (self.speed == 83 and len(self.doorstepNum) >= 1) or len(self.doorstepNum) >= 3:
            filehandle.write('Die Angabe der Tuerschwellen ist mit Vorsicht zu genießen!\n')
    
    def genLogFile(self):
        # test
        #fullpath = str('EVAL_' + self.filename + '.txt')
        # running system
        fullpath = str(self.filepath + 'EVAL_' + self.filename + '.txt')
        self.filehandle = open(fullpath, 'w')
        self.filehandle.write('Auswertung fuer Datei: ' + self.filename + '\n')
        self.displayDoorSteps(self.filehandle)
        self.displayRoughness(self.filehandle)
        self.filehandle.close()
        rospy.loginfo("generated eval file")


if __name__ == '__main__':
    rospy.init_node('evalIMU')
    rospy.loginfo("started IMUeval node")
    IMUeval()
    rospy.spin()
    # i = IMUeval()
    # i.callbackFilepath()
    # i.detectDoorSteps()
    # i.genLogFile()
    