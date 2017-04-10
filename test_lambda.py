#!python -W ignore  -m unittest test_lambda

# for new-style print(...)
from __future__ import print_function

import csv
import sys
import unittest

from lambda_code import lambda_handler;

import numpy as np;
from numpy.random import multivariate_normal as norm

def createEvent( location, variance=1.0, prior={}, origin='gps' ):
    result = {
        'origin': origin,
        'latitude': location[0],
        'longitude': location[1],
        'variance': variance};
    if prior:
        result['prior']= prior

    return result;

class TestLambda(unittest.TestCase):

    def test_initial_filter( self):
        # pass in first point: without previous state continuity
        #print( "    (" +str(self.measurements[0][0])+", "+str(self.measurements[0][1])+")")
        event = createEvent( [ 23.3291, 44.3291], variance=10.0)

        result = lambda_handler( event, None);

        self.assertEqual( result['latitude'], event['latitude'])
        self.assertEqual( result['longitude'], event['longitude'])
        self.assertEqual( result['variance'], event['variance']);


    def test_single_update( self):

        firstEvent = createEvent( [ 23.3291, 44.3291])
        secondEvent = createEvent( [ 23.4227, 44.4227], prior = firstEvent )
        # print('    >> event[0]= [{}, {}]: {}'.format( firstEvent['latitude'], firstEvent['longitude'], firstEvent['variance']))
        # print('    >> event[1]= [{}, {}]: {}'.format( secondEvent['latitude'],secondEvent['longitude'],secondEvent['variance']))

        # simulate first call:
        result = lambda_handler( secondEvent, None);

        expected = {
            'latitude': 23.3915,
            'longitude': 44.39152286,
            'variance': 0.666666666667
        }

        # print("    << result=   [{}, {}]: {}".format( expected['latitude'], expected['longitude'], expected['variance']))
        self.assertAlmostEqual( result['latitude'], expected['latitude'], places=4, msg="latitude mismatch from filter!")
        self.assertAlmostEqual( result['longitude'], expected['longitude'], places=4, msg="longitude mismatch from filter!")
        self.assertAlmostEqual( result['variance'], expected['variance'], places=4)


    def test_multiple_update( self):
        measurement_count = 60;
        initial_truth = np.array([ 24, 45])
        error_variance = 5.0;
        error_covariance = np.multiply( error_variance, np.identity(2))
        measurements = norm( mean= initial_truth, cov=error_covariance, size = measurement_count)

        # pass in first point: without previous state continuity
        priorEvent = None
        events=[];
        results=np.empty_like( measurements )
        resultIndex = 0
        for location in measurements:
            currentEvent = createEvent( location, prior = priorEvent )

            result = lambda_handler( currentEvent, None)

            results[resultIndex] = [ result['latitude'], result['longitude']]
            resultIndex += 1

            # if 'prior' in currentEvent:
                # print("....[{:>8.6}, {:>8.6}] => [{:>8.6}, {:>8.6}]( {:>6.6})".format(
                #     location[0], location[1],
                #     currentEvent['prior']['latitude'], currentEvent['prior']['longitude'], currentEvent['prior']['variance']))
                # print("........................... [{:>8.6}, {:>8.6}]( {:>6.6})".format(
                #     result['latitude'], result['longitude'], result['variance']))

            priorEvent = result

        # print( results )
        self.assertAlmostEqual( result['latitude'], initial_truth[0], delta=5)
        self.assertAlmostEqual( result['longitude'], initial_truth[1], delta=5)
        self.assertAlmostEqual( result['variance'], 1, delta = 2)


if __name__ == '__main__':
    unittest.main()
