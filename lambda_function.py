import json
import psycopg2
from datetime import date
import datetime


def lambda_handler(event, context):

    print('a')
   
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
