# ###########################################################################################
# README.txt
# ###########################################################################################
# Author: Alexander Hrabski (ahrabski@umich.edu)
# Purpose: Outlines the useage of the operations-focused tidalfilterlib
# Last update: 01/2023 Alexander Hrabski (ahrabski@umich.edu)
# ###########################################################################################

The library of functions contained in tidalfilterlib.py is intended to greatly simplify the
application of the methods developed with the research-focused ETSSfilteringlib. It contains 
two functions (as well as a support function) which produce anomaly forecasts and signal-to-noise
ratios, respectively, using (and accepting) identical parameters to the 2023 extended abstract
on this method.

AnomalyCorrection14Day(anomaly_hindcast,input_hindcast,input_forecast):

    anomaly_hindcast -->    a numpy array containing 14 days of hindcast anomaly, with 1 hour
                            spacing between data points.

    input_hindcast -->      input to the filter (the ETSS tide signal in the 2023 study).
                            data must be of equal length at equal times to the anomaly_hindcast.
                            also a numpy array

    input_forecast  -->     a numpy array of the input shifted by 102 hours into the future, as 
                            described in the 2023 extended abstract. 

    returns 

    anomaly_forecast -->    the anomaly forecast as a numpy array, of identical length and times
                            to the input_forecast array

EvaluateS2N14Day(anomaly_hindcast):

    anomaly_hindcast -->    a numpy array containing 14 days of hindcast anomaly, with 1 hour
                            spacing between data points.

    returns

    S2N -->                 the signal-to-noise ratio, as defined in the 2023 extended abstract.
