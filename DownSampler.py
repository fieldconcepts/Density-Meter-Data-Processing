import csv
import numpy as np
import matplotlib.pyplot as plt
import wx
import os

from itertools import islice


downsampled = []

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




with open(datafile) as fin:
    csvin = csv.reader(fin)
    # Skip header, and then return every 100th until file ends
    for line in islice(csvin, 1, None, 100):
        downsampled.append(line)



with open("output.csv", "wb") as f:
    writer = csv.writer(f)
    writer.writerows(downsampled)