# ############################################################################################
# validate.py
# ############################################################################################
# Author: Alexander Hrabski (ahrabski@umich.edu)
# Purpose: Validate the tidalfilterlib against the research-focused ETSSfilteringlib
# Last update: Alexander Hrabski 01/2023
# ############################################################################################
import numpy as np
import matplotlib.pyplot as plt
from sys import path

##Provide paths and parameters
path2ETSSlib = '../'

startdate = '20220424'
stopdate = '20220507'
txxz = '12'

date = '05/08/2022'

window = 2
lowpass = 100
S2Ncutoff = 1.5
input_field = 'TIDE'

station_id = '8534638'

datapath = '../../../'
masterpath = '../../../'

##Load libraries
path.insert(0,path2ETSSlib)
from station import slist, station, GetXTicks
import tidalfilterlib

##Generate ETSSfilteringlib anomaly forecast
stations = slist(masterpath, path2data = datapath, ID_list=[station_id])

s = stations[0]
s.normalize_filter = True
s.lowpass = lowpass
s.harmonicpass = window
s.S2Ncutoff = S2Ncutoff
s.new_mean = 0
s.ForecastAnomaly(input_field,startdate=startdate,stopdate=stopdate,txxz=txxz,reset=True)

##Generate tidalfilterlib anomaly forecast
tide_hindcast = s['TIDE']
tide_forecast = s['TIDE_FORECAST']
anomaly_hindcast = s['BIAS']

anomaly_forecast = tidalfilterlib.AnomalyCorrection14Day(anomaly_hindcast,tide_hindcast,tide_forecast)

##Set 0-mode (avg. value) for validation
validate = s['BIAS_CORRECTION']
zeromode = np.fft.fft(validate)[0]
anomaly_forecast = np.fft.fft(anomaly_forecast)
anomaly_forecast[0] = zeromode
anomaly_forecast = np.real(np.fft.ifft(anomaly_forecast))

##Report the S2N ratios and relative error
print('S2N:                {}'.format(tidalfilterlib.EvaluateS2N14Day(anomaly_hindcast)))
print('S2N (original lib): {}'.format(s.CheckS2N()))
print('% error vs. ETSSfilteringlib: {}'.format(np.max(np.abs(anomaly_forecast-validate)/validate)*100))

##Generate an example figure
fig,ax=plt.subplots(1,1,figsize=[10.0*1.5,4.8*0.90])
ax.plot(s['BIAS_CORRECTION_TIME'][-102:],anomaly_forecast[-102:],'g',label='anomaly') #[-102:] selects only the 102 hour forecast interval.
ax.plot(s['BIAS_TIME'],anomaly_hindcast,'g')
ax.scatter(s['BIAS_CORRECTION_TIME'][-102:],validate[-102:],s=10,c='r',marker='x',label='ETSSfilteringlib')

ax.plot(s['TIDE_TIME'],tide_hindcast,'b')
ax.plot(s['TIDE_FORECAST_TIME'][-102:],tide_forecast[-102:],'b',label='tide')

ylim = ax.get_ylim()
ax.plot(2*[14*24],ylim,'r',zorder=3)
ax.set_xlabel('Time (UTC)')
ax.set_ylabel('Height over MLLW [ft.]')
ax.set_title('{} {}, {} {}:00 UTC'.format(s['Station Name'], s['Station ID'], date, txxz))
tick_pos,tick_str = GetXTicks(startdate,stopdate,txxz)

ax.set_xticks(tick_pos)
ax.set_xticklabels(tick_str)
plt.legend()
plt.show()
