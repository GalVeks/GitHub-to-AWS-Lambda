import pandas as pd
import json
import numpy as np
import requests
import psycopg2
from datetime import date
import datetime
import main


def lambda_handler(event, context):
    # Create Postgres SQL connection (Parameters should be stored in KMS)

    #account_scrape = str(event['queryStringParameters']['account'])

    connection = psycopg2.connect(user="postgres",
                                  password="postgres",
                                  host="devpostgres01.cphbkxf9hicq.us-east-1.rds.amazonaws.com",
                                  port="5432",
                                  database="postgres")
    cursor = connection.cursor()

    # Get last Runbook id
    cursor.execute('''select coalesce (max(run_id) + 1 , 1)
                        from "SP_ADMIN".ref_runbook_history''')
    result = cursor.fetchone()
    idx = str(result[0])

    # Define insert query (to factorization later)
    postgres_insert_query = """ INSERT INTO "SP_ADMIN".ref_runbook_history (RUN_ID, 
                                                            CATEGORY, 
                                                            DISPLAY_NAME, 
                                                            AS_OF_DATE, 
                                                            START_TIME, 
                                                            END_TIME, 
                                                            STATUS, 
                                                            DURATION) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"""

    record_to_insert = (idx,
                        'Instagram',
                        'DISPLAY_NAME',
                        date.today(),
                        datetime.datetime.now()
                        , datetime.datetime.now()
                        , 'Failed'
                        , datetime.datetime.now() - datetime.datetime.now())

    # Commit query
    cursor.execute(postgres_insert_query, record_to_insert)
    connection.commit()
    count = cursor.rowcount
    print(count, "Record inserted successfully into mobile table")

    ##########################################
    # Put your code in this block
    ##########################################
    
    #main.main_run(account_scrape)

    ##########################################
    ##########################################

    return {
        'statusCode': 200,
        'body': event #json.dumps('ok')#'Scrape account: {}'.format(account_scrape))
      }




