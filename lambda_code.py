#!python

import math
import json
import sys

sys.path.append("./libs")
import numpy as np
from pykalman import KalmanFilter

# CONSTANT PARAMETERS

TRANSITION_MATRIX = np.eye( 2)
OBSERVATION_MATRIX = np.eye( 2)
COVARIANCE_MATRIX = np.eye( 2)

# yes, this is a magic number.  It's very roughly based on how far
# a device receiver might be from the cell tower, but is only accurate to a ROM.
CELL_VARIANCE = 2500.0 # in meters
GPS_VARIANCE = 10.0 # in meters

# EVENT I/O KEYS
MEASUREMENT_KEY = 'now'
PREVIOUS_STATE_KEY = 'prior'
LATITUDE_KEY = 'latitude'
LONGITUDE_KEY = 'longitude'
VARIANCE_KEY = 'variance'

def get_variance( event ):
    if 'origin' in event:
        if 'cel' in event['origin']:
            # if this is a cell tower, degreed the effective accuracy
            return CELL_VARIANCE

    return GPS_VARIANCE


# possibly refactor to a more efficient version:
# http://scottlobdell.me/2014/08/kalman-filtering-python-reading-sensor-input/

def process_update( measure, variance, prev_state, prev_cov ):
    return (measure, variance);


def lambda_handler(event, context):
    # Log the received event
    #   implement me!

    try:
        variance = get_variance( event )

        if (PREVIOUS_STATE_KEY in event):
            prev = event[PREVIOUS_STATE_KEY];
            prevMean = np.array([ prev[LATITUDE_KEY], prev[LONGITUDE_KEY]])
            prevCovar = np.multiply( prev[VARIANCE_KEY], COVARIANCE_MATRIX )


            kf = KalmanFilter(
                initial_state_mean=prevMean,
                initial_state_covariance=prevCovar,
                em_vars=['transition_covariance', 'observation_covariance'],
                transition_matrices=TRANSITION_MATRIX)


            curObs = np.array([ event[LATITUDE_KEY], event[LONGITUDE_KEY]]);
            curCovar = np.multiply( event[VARIANCE_KEY], np.eye( len(curObs)))

            nextMean, nextCovar = kf.filter_update(
                prevMean,
                prevCovar,
                observation_matrix=OBSERVATION_MATRIX,
                observation=curObs,
                observation_covariance=curCovar)

            return {
                LATITUDE_KEY: nextMean[0],
                LONGITUDE_KEY: nextMean[1],
                VARIANCE_KEY: nextCovar[0][0],
            }


        else:
            # if first point in sequence...
            # just return the single location point, with corresponding accuracy
            return {
                LATITUDE_KEY: event[LATITUDE_KEY],
                LONGITUDE_KEY: event[LONGITUDE_KEY],
                VARIANCE_KEY: variance
            }

    except Exception as e:
        print(e)
        return { 'message': str(e) }
