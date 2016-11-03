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


adc_range = 65535
adc_voltage = 2.5
temp_gain = 31.30303

	

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


#----PLOTTING GRAPH STUFF---------

time = [row for row in timestamp]
tempdataX = [row for row in tempdata]
presdataX = [row for row in presdata]
realtempX = [row for row in realtemp]

plt.figure(1)
plt.subplot(311)
plt.title('DMS Raw Data (File: ' + tail +')')
plt.plot(time, presdataX, 'b-')
plt.ylabel('Diff Pres')
plt.grid(True)

plt.subplot(312)
plt.plot(time, tempdataX, 'y-')
plt.ylabel('Diff Rtd')
plt.grid(True)

plt.subplot(313)
plt.plot(time, realtempX, 'g-')
plt.ylabel('Real Temp (C)')
plt.xlabel('Time (Minutes)')
plt.grid(True)

plt.show()







