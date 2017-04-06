#!python
from __future__ import print_function

import boto3
import json
import sys

sys.path.append("./libs")
import requests

print('Loading function')

batch = boto3.client('batch')

def lambda_handler(event, context):
    # Log the received event
    print("Received event: " + json.dumps(event, indent=2))

    try:
        # Call DescribeJobs
        print("value1 = " + event['key1'])
        print("value2 = " + event['key2'])
        print("value3 = " + event['key3'])
        return "Hello World!";
    except Exception as e:
        print(e)
        message = 'Error getting Batch Job status'
        print(message)
        raise Exception(message)
