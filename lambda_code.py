#!python
from __future__ import print_function

import math
import json
import sys

sys.path.append("./libs")

import numpy as np

# CONSTANT PARAMETERS

TRANSITION_MATRIX = np.eye( 2)
OBSERVATION_MATRIX = np.eye( 2)

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
            return 1000;

    return 1.0


# possibly refactor to a more efficient version:
# http://scottlobdell.me/2014/08/kalman-filtering-python-reading-sensor-input/

def process_update( measure, variance, prev_state, prev_cov ):
    return (measure, variance);


def lambda_handler(event, context):
    # Log the received event
    #   implement me!

    # print("Received event:");
    # for key, value in event.items():
    #     print("    [{}] = {}".format( key, value))

    try:
        variance = get_variance( event )

        if (PREVIOUS_STATE_KEY in event):
            print("....detected previous state:")
            prev = event[PREVIOUS_STATE_KEY];
            prevMean = np.array([ prev[LATITUDE_KEY], prev[LONGITUDE_KEY]])
            prevCovar = np.multiply( prev[VARIANCE_KEY], np.eye( S0.shape[0]) )

            print('    ??: {} <= {}'.format( prevMean, prevCovar ))
            kf = KalmanFilter(
                initial_state_mean=prevMean,
                initial_state_covariance=prevCovar,
                em_vars=['transition_covariance', 'observation_covariance'],
                transition_matrices=TRANSITION_MATRIX)

            print('   ?? kf: '+str(kf))

            curObs = np.array([ event[LATITUDE_KEY], event[LONGITUDE_KEY]]);
            curCovar = np.multiply( event[VARIANCE_KEY], np.eye( len(curObs)))

            nextMean, nextCovar = kf.filter_update(
                prevMean,
                prevCovar,
                observation_matrix=OBSERVATION_MATRIX,
                observation=curObs,
                observation_covariance=curCovar)

            print('   ?? next_state: '+str( prevMean))
            print('   ?? next_covar: '+str( prevCovar))

            return {
                LATITUDE_KEY: 1.,
                LONGITUDE_KEY: 1.,
                VARIANCE_KEY: 0.,
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
