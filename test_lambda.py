#!python

# for new-style print(...)
from __future__ import print_function

import csv
import sys
import unittest


from lambda_code import lambda_handler;

import numpy as np;
from numpy.random import multivariate_normal as norm

def createEvent( latitude, longitude, variance=1.0, prior={}, origin='gps' ):
    result = {
        'origin': origin,
        'latitude': latitude,
        'longitude': longitude,
        'variance': variance};
    if prior:
        result['prior']= prior

    return result;

class IntentTestCase(unittest.TestCase):

    def setUp(self):
        measurement_count = 20;

        initial_truth = np.array([ 24, 45])

        error_variance = 1.0;
        error_covariance = np.multiply( error_variance, np.ones([2,2]));

        # isn't numpy cool?
        self.measurements = norm( mean= initial_truth, cov=error_covariance, size = measurement_count)

    def test_initial_filter( self):
        # pass in first point: without previous state continuity
        #print( "    (" +str(self.measurements[0][0])+", "+str(self.measurements[0][1])+")")
        event = createEvent( self.measurements[0][0], self.measurements[0][1] )

        result = lambda_handler( event, None);

        self.assertEqual( result['latitude'], self.measurements[0][0]);
        self.assertEqual( result['longitude'], self.measurements[0][1]);
        self.assertEqual( result['variance'], 1.0);


    def test_next_call( self):
        pass
        # print( "running Kalman Filter update: ");
        #
        # # pass in first point: without previous state continuity
        # #print( "    (" +str(self.measurements[0][0])+", "+str(self.measurements[0][1])+")")
        # events=[];
        # events.append( createEvent( self.measurements[0][0], self.measurements[0][1]))
        # events.append( createEvent( self.measurements[1][0], self.measurements[1][1], prior = events[0]))
        #
        # # print("..event[0]: {}".format( events[0]));
        # # print("..event[1]: {}".format( events[1]));
        #
        # result = lambda_handler( events[1], None);
        #
        # print( result );
        #
        # self.assertEqual( result['latitude'], self.measurements[0][0]);
        # self.assertEqual( result['longitude'], self.measurements[0][1]);
        # self.assertEqual( result['variance'], 1.0);
        #
        # print( result );



if __name__ == '__main__':
    unittest.main()
