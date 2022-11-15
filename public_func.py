from io import StringIO  # python3; python2: BytesIO
import boto3
import pandas as pd
import yfinance as yf


def save_pd_csv_to_s3(bucket='mdm-social-project', df='', key=''):
    csv_buffer = StringIO()
    df.to_csv(csv_buffer)
    s3_resource = boto3.resource('s3')
    s3_resource.Object(bucket, key).put(Body=csv_buffer.getvalue())

