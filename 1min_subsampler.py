# This is a script to sub sample data from the ESP NXTGEN ESP Sensory & FLow Metering log files. 
# The tool logs a dataframe to file approximately every 1.1 seconds resulting in duplicate dataframes occuring with time
# To reduce dataset size to and streamline processing this script will take data, remove duplicates and output
# 1 minute data to csv file.
# 17-11-2017
# Ben Kaack


import csv
import wx
import os

downsampled = []
checklist = set()

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

datafile = get_path('*.dat;*.txt;*.csv;*.log;')


with open(datafile) as fin:
    csvin = csv.reader(fin)
    # ESP Intake Abs PSI = 0
    # ESP Intake Abs Temp = 1
    # DMS Intake Diff PSI  = 2
    # DMS Intake Diff Temp = 3
    # VEN Discharge Abs PSI = 4
    # VEN Discgarge Abs Temp = 5
    # VEN Discharge Diff PSI = 6
    # VEN Discharge Diff Temp = 7
    # Time(GMT) = 22
    
    for line in csvin:
        time = line[22]
        
        #sub-sample every minute
        if time[6:] == "00":
            
            #remove duplicates using checklist set()
            if time not in checklist:
                downsampled.append(line)
                checklist.add(time)

            
with open("1minute_sample.csv", "wb") as f:
    writer = csv.writer(f)
    writer.writerows(downsampled)