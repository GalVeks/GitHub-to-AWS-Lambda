import pandas as pd
import json
import numpy as np
import requests
import psycopg2
from datetime import date
import datetime
import uuid
import main


def lambda_handler(event, context):
    # Create Postgres SQL connection (Parameters should be stored in KMS)

    account_scrape = "galvekselman"  # str(event['queryStringParameters']['Account'])
    event_scrape = "/igFollowers"  # str(event['rawPath'])

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

    run_timestamp = datetime.datetime.now()

    # Define insert query (to factorization later)
    postgres_insert_query = """ INSERT INTO "SP_ADMIN".ref_runbook_history (RUN_ID, 
                                                            CATEGORY, 
                                                            DISPLAY_NAME, 
                                                            AS_OF_DATE, 
                                                            START_TIME, 
                                                            END_TIME, 
                                                            STATUS, 
                                                            DURATION,
                                                            PAYLOAD) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"""

    record_to_insert = (idx
                        , event_scrape
                        , account_scrape
                        , date.today()
                        , run_timestamp
                        , run_timestamp
                        , 'RUNNING'
                        , run_timestamp - run_timestamp
                        , 'RUNNING')

    # Commit query
    cursor.execute(postgres_insert_query, record_to_insert)
    connection.commit()
    count = cursor.rowcount
    print(count, "Record inserted successfully into runbook table")

    try:
        ##########################################
        # Put your code in this block
        ##########################################

        # Scrape follower by account
        if event_scrape == "/igFollowers":
            print("Start scraping follower of :" + account_scrape)
            main.main_run(account_scrape)

        ##########################################
        postgres_insert_query = """ UPDATE "SP_ADMIN".ref_runbook_history 
                                            SET status = 'SUCCEEDED'
                                            ,end_time = %s
                                            ,duration = %s
                                            ,payload = %s
                                            WHERE run_id = %s """

        record_to_insert = (datetime.datetime.now()
                            , datetime.datetime.now() - run_timestamp
                            , "Account: " + account_scrape
                            , idx
                            )

        # execute the query
        cursor.execute(postgres_insert_query, record_to_insert)
        connection.commit()
        count = cursor.rowcount

        print(count, "Record updated successfully into runbook table")
    except Exception as e:

        postgres_insert_query = """ UPDATE "SP_ADMIN".ref_runbook_history 
                                    SET status = 'FAILED'
                                    ,end_time = %s
                                    ,duration = %s
                                    ,payload = %s
                                    WHERE run_id = %s """

        record_to_insert = (datetime.datetime.now()
                            , datetime.datetime.now() - run_timestamp
                            , str(e)
                            , idx
                            )

        # execute the query
        cursor.execute(postgres_insert_query, record_to_insert)
        connection.commit()
        count = cursor.rowcount

        print(count, "Record updated successfully into runbook table")

    ##########################################

    return {
        'statusCode': 200,
        'body': json.dumps('ok')  # 'Scrape account: {}'.format(account_scrape))
    }


