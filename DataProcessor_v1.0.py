import numpy as np
import matplotlib.pyplot as plt
import wx


#Promt user to select scope trace for analysis
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

datafile = get_path('*.txt;*.csv')



#----IMPORT DATA SETS FROM TXT FILE----------

tempdata = np.genfromtxt(datafile, delimiter=',', dtype='int32', usecols = 0)   #import column 1 temp data from data set
presdata = np.genfromtxt(datafile, delimiter=',', dtype='int32', usecols = 1)   #import column 2 pressure data from data set





#----CALCULATING THE TIME DOMAIN SAMPLE RATE----------

numofsamples = tempdata.size  #find how many samples were taken
ls = (numofsamples - 1) * 0.018433   # sample rate = 1.106 secs   = 0.018433 minutes
timestamp = np.linspace(0, ls, num=numofsamples)  #create a time array samplerate adjsuted to 1.106s




#----PLOTTING GRAPH STUFF---------



#plot columns to axis
time = [row for row in timestamp]
tempdataX = [row for row in tempdata]
presdataX = [row for row in presdata]


plt.figure(1)
plt.subplot(211)
plt.plot(time, presdataX, 'b-')
plt.ylabel('Pressure')
plt.grid(True)


plt.subplot(212)
plt.plot(time, tempdataX, 'y-')
plt.ylabel('Temp')
plt.xlabel('Time (Minutes)')
plt.grid(True)


plt.show()







