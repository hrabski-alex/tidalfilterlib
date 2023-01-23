# ############################################################################################
# tidalfilterlib.py
# ############################################################################################
# Author: Alexander Hrabski (ahrabski@umich.edu)
# Purpose: Generate oscillating anomaly forecasts given anomaly and tide hindcasts
# Last update: Alexander Hrabski 01/2023
# ############################################################################################
import numpy as np

def AnomalyCorrection14Day(anomaly_hindcast,input_hindcast,input_forecast):

    ##Set required post-processor parameters
    dt = 1. #in hours
    df_input = 15. #in deg/hr
    window = 2. #in deg/hr
    lowpass = 100. #in deg/hr

    ##Define resolved frequencies
    freq = np.fft.fftfreq(anomaly_hindcast.size,d = dt) * 360.

    ##Move to Fourier-domain
    anomaly_hindcast_hat = np.fft.fft(anomaly_hindcast)
    input_hindcast_hat = np.fft.fft(input_hindcast)
    input_forecast_hat = np.fft.fft(input_forecast)

    ##Synthesize filter
    h_hat = anomaly_hindcast_hat/input_hindcast_hat

    ##Bandpass filter
    log = bandpass(freq,df_input,window)
    h_hat[log] = 0.

    ##Lowpass filter
    log = np.abs(freq) > lowpass
    h_hat[log] = 0.

    ##Normalize amplitudes
    h_hat = h_hat * np.abs(input_hindcast_hat)/np.abs(input_forecast_hat)

    ##Set mean to zero
    h_hat[0] = 0.

    ##Apply filter
    anomaly_forecast_hat = h_hat * input_forecast_hat

    ##Move to time-domain
    anomaly_forecast = np.real(np.fft.ifft(anomaly_forecast_hat))

    return anomaly_forecast

##Check Signal to noise ratio
def EvaluateS2N14Day(anomaly_hindcast):

    ##Set required post-processor parameters
    dt = 1. #in hours
    df_input = 15. #in deg/hr
    window = 2. #in deg/hr
    lowpass = 100. #in deg/hr

    ##Define resolved frequencies
    freq = np.fft.fftfreq(anomaly_hindcast.size,d = dt)[1:] * 360. #exclude 0-mode

    ##Move to Fourier-domain
    anomaly_hindcast_hat = np.fft.fft(anomaly_hindcast)/anomaly_hindcast.size
    anomaly_hindcast_hat = anomaly_hindcast_hat[1:] #exclude 0-mode

    ##Bandpass filter
    log = bandpass(freq,df_input,window)
    
    ##Lowpass filter
    log_lp = np.abs(freq) > lowpass

    ##Combine filtering steps
    log = np.logical_or(log_lp, log)     

    nlog = np.logical_not(log)

    ##Compute signal and noise power
    noise = np.sum(np.abs(anomaly_hindcast_hat[log])**2)
    signal = np.sum(np.abs(anomaly_hindcast_hat[nlog])**2)

    ##Return S2N
    return signal/noise

def bandpass(freq,df_input,window):
    ##Generate bandpass logical array
    f = df_input
    log = np.full(freq.size,False)

    if df_input >= np.max(freq):
        raise ValueError('Maximum frequency cannot be less than tidal frequency spacing.')

    while f < np.max(freq):
        log1 = np.abs(freq) > f - window
        log2 = np.abs(freq) < f + window
        log = np.logical_or(log,np.logical_and(log1,log2))
        f += df_input

    log = np.logical_not(log)
    return log
