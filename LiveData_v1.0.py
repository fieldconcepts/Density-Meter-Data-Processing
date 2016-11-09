import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time
import wx
import os


#Select File UX Function
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


#Animation Function
def animate(i): 
	
	pullData = open(datafile,"r").read()
	dataArray = pullData.split('\n')
	
	timear = [] #timestamp array
	xar = [] #transducer array
	yar = [] #rtd array
	presar = [] #pressure array
	tempar = [] #temp array
	
	count = 1
	
	for eachLine in dataArray:
	
		if len(eachLine)>1:
		
			newLine = eachLine + " " + str(count)
			x,y,t = newLine.split(';')
			
			transducer = int(x) #raw transducer output
			rtd = int(y)		#raw rtd output
			timestamp = int(t)	#sample number (starting from 1)
			
			timemin = timestamp * 0.018433   # convert to proper timestamp in minutes. Sample rate = 1.106 secs = 0.018433 minutes
			timear.append(timemin) #append time in minutes to array
			
			xar.append(transducer) 	#append transducer output to array
			yar.append(rtd)			#append rtd output to array
			
			
			#---- Calibration Constants---
			adc_range = 65535
			adc_voltage = 2.5
			temp_gain = 31.30303
			pres_gain = 12.547344
			
			
			#----Convert to Real Temp-----------------
			Tvolt = 2.5 + ((rtd*(adc_voltage/adc_range))/temp_gain) 
			VOhm = ((Tvolt*10000)/(5-Tvolt))-9000
			realTemp = (VOhm-1000)/3.9
			
			tempar.append(realTemp)	#append Real Temperature to array
			
			#----Convert to pressure-----
			offsetpres = transducer - 5531 #Pressure transducer Offset. Important! This number needs to be set after each vac fill.
			outputVDC = offsetpres * ((adc_voltage/adc_range)/(0.5 * pres_gain))
			
			
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
			
			
			#---- Polynomial
			realpres = a + (b*outputVDC) + (c*VOhm) + (d*(outputVDC**2)) + (e*(VOhm**2)) + (f*outputVDC*VOhm) + (g*(outputVDC**3)) + (h*(VOhm**3)) + (i*outputVDC*(VOhm**2)) + (j*(outputVDC**2)*VOhm)
			
			presar.append(realpres)		#append Real Pressure to array	
			
			count += 1	

	ax1.clear()
	ax2.clear()
	ax3.clear()
	ax4.clear()
	

	ax1.plot(timear,xar, 'b-')
	ax1.set_title('DMS Raw Data (File: ' + tail +')')
	ax1.set_ylabel('Sensor')
	ax1.grid(True)
	
	ax2.plot(timear,yar, 'y-')
	ax2.set_ylabel('Rtd')
	ax2.grid(True)
	
	ax3.plot(timear,presar,'r-')
	ax3.set_ylabel('PSIG')
	ax3.grid(True)
	
	
	ax4.plot(timear,tempar, 'g-')
	ax4.set_ylabel('Temp(C)')
	ax4.set_xlabel('Minutes')
	ax4.grid(True)

	
#trigger function to select file
datafile = get_path('*.txt;*.csv;*.log;') 
head, tail = os.path.split(datafile)


# Plotting graph
fig = plt.figure()
ax1 = fig.add_subplot(4,1,1)
ax2 = fig.add_subplot(4,1,2)
ax3 = fig.add_subplot(4,1,3)
ax4 = fig.add_subplot(4,1,4)


#Animate graph by refreshing every xxxx milliseconds
ani = animation.FuncAnimation(fig, animate, interval=2000)
plt.show()
