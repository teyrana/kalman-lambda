#!python

# for new-style print(...)
from __future__ import print_function

import csv
import sys
import unittest


import lambda_code;

import numpy;



class IntentTestCase(unittest.TestCase):


    def setUp(self):
        truth = ( 24, 45);

        print( "Generating random test inputs, centered around "+str(truth));
        # random generates data on [0,1)
        error = numpy.random.rand( 20,2)
        self.measurements = numpy.add( truth, error)
        self.kf = lambda_code.lambda_handler


        # numpy.savetxt( 'measurements.csv', measured, fmt="%6.4f", delimiter=',')


    def test_simple_response( self):
        self.assertEqual( self.measurements.shape, (20,2));

# assertEqual(a, b) 	a == b
# assertNotEqual(a, b) 	a != b
# assertTrue(x) 	bool(x) is True
# assertFalse(x) 	bool(x) is False
# assertIs(a, b) 	a is b 	2.7
# assertIsNot(a, b) 	a is not b 	2.7
# assertIsNone(x) 	x is None 	2.7
# assertIsNotNone(x) 	x is not None 	2.7
# assertIn(a, b) 	a in b 	2.7
# assertNotIn(a, b) 	a not in b 	2.7
# assertIsInstance(a, b) 	isinstance(a, b) 	2.7
# assertNotIsInstance(a, b) 	not isinstance(a, b) 	2.7

    def test_first_call( self):
        pass
        #self.kf()



if __name__ == '__main__':
    unittest.main()
