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



#----IMPORT CH1 DATA SETS FROM TXT FILE----------

timestamp = np.genfromtxt(datafile, delimiter='\t', dtype='float', usecols = 0, skip_header=2)   #import column 1 temp data from data set
CH1G = np.genfromtxt(datafile, delimiter='\t', dtype='float', usecols = 1, skip_header=2)   #import column 2 pressure data from data set
axis_name1 = tail

#----CALCULATING THE TIME DOMAIN SAMPLE RATE----------

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

#----IMPORT CH2 DATA SETS FROM TXT FILE----------

CH2G = np.genfromtxt(datafile, delimiter='\t', dtype='float', usecols = 1, skip_header=2)   #import column 2 pressure data from data set
axis_name2 = tail

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
modbustime =  np.genfromtxt(datafile, delimiter=',', dtype='float', usecols = 22, skip_header=0)

numofsamples = XaxisG.size  #find how many samples were taken

timestampMod = np.linspace(0, numofsamples, num=numofsamples)  #create a time array samplerate adjsuted to 1.106s 

#----PLOTTING GRAPH STUFF---------

time = [row for row in timestamp]
CH1realG = [row for row in CH1G]
CH2realG = [row for row in CH2G]

Xaxis = [row for row in XaxisG]
Zaxis = [row for row in ZaxisG]
timemod = [row for row in timestampMod]

plt.figure(1)
plt.subplot(311)
plt.title('Vibration Data (File: ' + axis_name1 +')')
plt.plot(time, CH1realG, 'b-')
plt.ylabel('CH1 Real [g]')
plt.grid(True)

plt.subplot(312)
plt.title('Vibration Data (File: ' + axis_name2 +')')
plt.plot(time, CH2realG, 'b-')
plt.ylabel('CH2 Real [g]')
plt.grid(True)

plt.subplot(313)
plt.title('Vibration Data (File: ' + tail +')')
plt.plot(timemod, Xaxis, 'r-')
plt.plot(timemod, Zaxis, 'g-')
plt.ylabel('Vibration [g]')
plt.xlabel('Time (Seconds)')
plt.legend(['X-axis', 'Z-axis'], loc='upper left')
plt.grid(True)



plt.show()







