
import pandas as pd
import json
import numpy as np
import requests

#import psycopg2
from datetime import date
import datetime

def lambda_handler(event, context):
    connection = psycopg2.connect(user="postgres",
                                  password="postgres",
                                  host="devpostgres01.cphbkxf9hicq.us-east-1.rds.amazonaws.com",
                                  port="5432",
                                  database="postgres")
    cursor = connection.cursor()

    postgres_insert_query = """ INSERT INTO "SP_ADMIN".ref_runbook_history (RUN_ID, 
                                                            CATEGORY, 
                                                            DISPLAY_NAME, 
                                                            AS_OF_DATE, 
                                                            START_TIME, 
                                                            END_TIME, 
                                                            STATUS, 
                                                            DURATION) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"""
    record_to_insert = ('1', 
                        'Instagram', 
                        'DISPLAY_NAME',
                        date.today(),
                        datetime.datetime.now()
                        ,datetime.datetime.now()
                        ,'Failed'
                        ,datetime.datetime.now() - datetime.datetime.now())
    cursor.execute(postgres_insert_query, record_to_insert)

    connection.commit()
    count = cursor.rowcount
    print(count, "Record inserted successfully into mobile table")

    return {
        'statusCode':200,
        'body': json.dumps('Hello from Lambda!')
    }

