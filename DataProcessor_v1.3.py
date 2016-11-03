#----------------------------------------------------
#Ben Kaack
#14/10/2016
#Python script for processing updated Density Meter Data sets in the Comma Delimuted format
#
#  5168,45661
#
#--------------------------------------------------



import numpy as np
import matplotlib.pyplot as plt
import wx
import os

#---- Calibration ---
adc_range = 65535
adc_voltage = 2.5
temp_gain = 31.30303
pres_gain = 12.547344


#---- Polynomial coefficients---
a =  -2149.40937555954
b =  81.2745013766329
c =  4.78657967494506
d =  26.7731700490019
e =  -0.00349450706916224
f =  0.0337724632307675
g =  17.3203989658766
h =  0.000000830545030845119
i =  -0.0000135239862347457
j =  -0.0223726317928853


#---- Density parameters-------

height = 3.048 #in meters
grav = 9.80655
	

#Promt user to select data file for analysis
def get_path(wildcard):
    app = wx.App(None)
    style = wx.FD_OPEN | wx.FD_FILE_MUST_EXIST
    dialog = wx.FileDialog(None, "Choose Data File", wildcard=wildcard, style=style)
    if dialog.ShowModal() == wx.ID_OK:
        path = dialog.GetPath()
    else:
        path = None
    dialog.Destroy()
    return path

datafile = get_path('*.txt;*.csv;*.log;')
head, tail = os.path.split(datafile)



#----IMPORT DATA SETS FROM TXT FILE----------

presdata = np.genfromtxt(datafile, delimiter=';', dtype='int32', usecols = 0)   #import column 1 temp data from data set
tempdata = np.genfromtxt(datafile, delimiter=';', dtype='int32', usecols = 1)   #import column 2 pressure data from data set


#----CALCULATING THE TIME DOMAIN SAMPLE RATE----------

numofsamples = tempdata.size  #find how many samples were taken
ls = (numofsamples - 1) * 0.018433   # sample rate = 1.106 secs   = 0.018433 minutes
timestamp = np.linspace(0, ls, num=numofsamples)  #create a time array samplerate adjsuted to 1.106s

#----Convert to Real Temp-----------------

Tvolt = 2.5 + ((tempdata*(adc_voltage/adc_range))/temp_gain) 
VOhm = ((Tvolt*10000)/(5-Tvolt))-9000
realtemp = (VOhm-1000)/3.9


#----Convert to pressure-----
offsetpres = presdata - 26172 #Pressure transducer Offset. Important! This number needs to be set after each vac fill.

outputVDC = offsetpres * ((adc_voltage/adc_range)/(0.5 * pres_gain))


#---Polynomial-----

realpres = a + (b*outputVDC) + (c*VOhm) + (d*(outputVDC**2)) + (e*(VOhm**2)) + (f*outputVDC*VOhm) + (g*(outputVDC**3)) + (h*(VOhm**3)) + (i*outputVDC*(VOhm**2)) + (j*(outputVDC**2)*VOhm)

#---Convert to Density---

realdens = (realpres*6894.75*0.001)/(height*grav)




#----PLOTTING GRAPH STUFF---------

time = [row for row in timestamp]
tempdataX = [row for row in tempdata]
presdataX = [row for row in presdata]
realtempX = [row for row in realtemp]
realpresX = [row for row in realpres]
realdensX = [row for row in realdens]

plt.figure(1)
plt.subplot(511)
plt.title('DMS Raw Data (File: ' + tail +')')
plt.plot(time, presdataX, 'b-')
plt.ylabel('Transducer Output')
plt.grid(True)

plt.subplot(512)
plt.plot(time, tempdataX, 'y-')
plt.ylabel('Rtd')
plt.grid(True)

plt.subplot(513)
plt.plot(time, realpresX, 'r-')
plt.ylabel('Diff Pressure (PSIG)')
plt.grid(True)

plt.subplot(514)
plt.plot(time, realtempX, 'g-')
plt.ylabel('Temp (C)')
plt.grid(True)

plt.subplot(515)
plt.plot(time, realdensX, 'g-')
plt.ylabel('Spec Grav')
plt.xlabel('Time (Minutes)')
plt.grid(True)

plt.show()







