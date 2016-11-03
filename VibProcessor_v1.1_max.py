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
import datetime
import csv



	



#----- Modbus Data FIle Import

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

XaxisG = np.genfromtxt(datafile, delimiter=',', dtype='float', usecols = 8, skip_header=0)   
ZaxisG = np.genfromtxt(datafile, delimiter=',', dtype='float', usecols = 9, skip_header=0)


modbustime =  np.genfromtxt(datafile, delimiter=',', dtype='string', usecols = 22, skip_header=0)

modbusdatetime = [datetime.datetime.strptime(elem, '%H:%M:%S') for elem in modbustime]



numofsamples = XaxisG.size  #find how many samples were taken

timestampMod = np.linspace(0, numofsamples, num=numofsamples)  #create a time array samplerate adjsuted to 1.106s 

#----PLOTTING GRAPH STUFF---------



Xaxis = [row for row in XaxisG]
Zaxis = [row for row in ZaxisG]
timemod = [row for row in timestampMod]

modbustimeX = [row for row in modbusdatetime]


plt.subplot(111)
plt.title('Vibration Data (File: ' + tail +')')
plt.plot(modbustimeX, Xaxis, 'r-')
plt.plot(modbustimeX, Zaxis, 'g-')
plt.ylabel('Surface Vibration [g]')
plt.xlabel('Time')
plt.legend(['X-axis', 'Z-axis'], loc='upper right')
plt.grid(True)



plt.show()







