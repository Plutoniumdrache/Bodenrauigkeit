#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
from numpy import genfromtxt


# In[2]:


raw_data = genfromtxt('Laborboden_quer_2Schwellen1_v84.csv', delimiter=',')
#ACHTUNG HIER IMMER NEUESTE DATEI EINLESEN


# In[3]:


# Überflüssige Werte abschneiden
for i in range(0,len(raw_data)):
    if raw_data[i][3]<raw_data[i-1][3]:
        Umdrehungen = raw_data[i-1][3]
        Umdrehungen_i = i-1
        break        
data = raw_data[:Umdrehungen_i]

#Fahrweg länge aus Umdrehungen berechnen
Fahrweg = 18*Umdrehungen/100
vek_Fahrweg = np.linspace(0,Fahrweg,len(data))


# In[4]:


#offset der z-Beschl.werte entfernen
z_mean = np.mean(data[:,2])
z_accel_clean = data[:,2]-z_mean


# In[5]:


# Ausreißer entfernen
# calculate borders with 3 sigma rule (2.2 sigma is used because of few data)
sigma = 2.2
negativeBorder = np.mean(z_accel_clean)-sigma*np.std(z_accel_clean)
positiveBorder = np.mean(z_accel_clean)+sigma*np.std(z_accel_clean)

# delete Data out of borders 
lower = np.where(z_accel_clean<negativeBorder)
z_accel_clean_woPeaks = np.delete(z_accel_clean,lower)
higher = np.where(z_accel_clean_woPeaks>positiveBorder)
z_accel_clean_woPeaks = np.delete(z_accel_clean_woPeaks,higher)


# In[6]:


#RMS über alle Werte nur für z

n1 = len(z_accel_clean_woPeaks) #Bereich festlegen
j = 0

while j < len(z_accel_clean_woPeaks)-n1+1:   
    square_z = 0  
    for i in range(0,n1):
        square_z += (z_accel_clean_woPeaks[j+i]**2)   
    mean_z = square_z/n1
    root_z = np.sqrt(mean_z)    
    j += i+1

root_z_ges = root_z


# In[7]:


#Klassifikator Versuch 2 Für alle V

speed = raw_data[0][4]    #ACHTUNG HIER MUSS IMMER DIE AKTUELLE GESCHWINDIGKEIT STEHEN
#EVT AUS CSV EINLESEN
#Grenzwerte
threshhold_85 = np.linspace(0,0.745,101)
threshhold_84 = threshhold_85 * 1.328770712165726
threshhold_83 = threshhold_84 * 1.040784135069001
# Rauigkeit bestimmen
if(speed == 85):
    for i in range(0,len(threshhold_85)):
        if(root_z_ges<=threshhold_85[i]):
            rauigkeit = i
            break
    if(root_z_ges>threshhold_85[100]):
        rauigkeit = 100
elif(speed == 84):
    for i in range(0,len(threshhold_84)):
        if(root_z_ges<=threshhold_84[i]):
            rauigkeit = i
            break
    if(root_z_ges>threshhold_84[100]):
        rauigkeit = 100 
elif(speed == 83):
    for i in range(0,len(threshhold_83)):
        if(root_z_ges<=threshhold_83[i]):
            rauigkeit = i
            break
    if(root_z_ges>threshhold_83[100]):
        rauigkeit = 100         

# Ausgabe der Rauigkeit und der Boden Vermutung
print('Die Rauigkeit des Bodens beträgt:',rauigkeit,'%')
if(rauigkeit<=26):
    print('Das entspricht z.B. Laborboden')
elif(rauigkeit<=31):
    print('Das entspricht z.B. Asphalt')
elif(rauigkeit<=41):
    print('Das entspricht z.B. Pflastersteinen')  
else:
    print('Das entspricht z.B. Kopfsteinpflaster')  


# In[8]:


#Türschwellen Erkennung

#RMS über festgelegte Anzahl an Werten für z
n = 3 #Bereich festlegen
root_vek_z = []
j = 0

while j < len(z_accel_clean)-n+1:
    square_z = 0    
    for i in range(0,n):
        square_z += (z_accel_clean[j+i]**2)
    mean_z = square_z/n
    root_z = np.sqrt(mean_z)    
    for i in range(0,n):
        root_vek_z.append(root_z)
    j += i+1
# Auffüllen der letzten Werte falls Gesamtanzahl nicht durch n Teilbar
while len(z_accel_clean)-len(root_vek_z):
    root_vek_z.append(root_vek_z[len(root_vek_z)-1])


# In[9]:


# Bodenschwellen detektieren

border = 3*np.mean(root_vek_z) 
doorstepNum = []
doorstepPos = []
j = 0
merker = 0

for i in range(0,len(root_vek_z)):
    if root_vek_z[i]> border and merker==0:  # vorher border
        if root_vek_z[i+1]<=border:
            break
        if root_vek_z[i+2]<=border:
            break
        #Anzahl der Türschwellen
        doorstepNum.append(j)
        #Position der Türschwellen
        doorstepPos.append(vek_Fahrweg[i])
        j +=1
        merker = 1
    # verhindert das aufeinanderfolgende Werte mehrere Türschwellen triggern    
    if root_vek_z[i]<=border:
        merker = 0  
        
#Ausgabe        
print('Es gibt',len(doorstepNum),'Türschwellen')
if len(doorstepNum):
    for i in range(0,len(doorstepNum)):
        print('Türschwelle',doorstepNum[i]+1,'bei',round(doorstepPos[i],1),'Metern')
if len(doorstepNum)== 2:
    if speed == 85:
        print('Korrigierter Rauigkeitswert:',rauigkeit-5,'%')
    elif speed ==84:
        print('Korrigierter Rauigkeitswert:',rauigkeit-10,'%')
if (speed == 83 and len(doorstepNum)>= 1) or len(doorstepNum)>= 3:
    print('Die Angabe der Türschwellen ist mit Vorsicht zu genießen!')
#HIER NOCHMAL AUSGEBEN WELCHEM BODENBELAG DAS ENTSPRECHEN KANN (BODENBELAGSAUSGABEFUNKTION AUFRUFEN)

