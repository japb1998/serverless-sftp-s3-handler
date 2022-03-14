# import os
# import sys
# import re
import boto3
import zipfile
import urllib.parse
from io import BytesIO 
import json



print('Loading function')

s3 = boto3.resource('s3')

# bucket_dev = s3.Bucket(bucket) 


def lambda_handler(event, context):
    # print("Received event: " + json.dumps(event, indent=2))

    # Get the object from the event and show its content type
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
    try:
        response = s3.Object(bucket_name=bucket, key=key)
        zip_obj = response.get()["Body"].read()
        # print('this is what comes from S3',zip_obj)
        buffer = BytesIO(zip_obj)
        
        # --------- handling json ----------
        # print('response',response)
        # print("CONTENT TYPE: " + response['ContentType'])
        # content_type = response['ContentType']
        # print(content_type)
        # print(response['Body'].read())
        
        print('afterIO' ,buffer)
        zfile = zipfile.ZipFile(buffer)
        with zfile as archive:
            print('this are the directories',archive.printdir())
            print('this is the zip file',zfile)
            # print(zfile.printdir())
            for filename in archive.namelist():
                # file_info = archive(filename)
                # print('this is a file ', filename)
                if filename.endswith('.json'):
                    with archive.open(filename,mode="r") as file:
                        data = file.read()
                        # print(data)
                        d = data.decode()
                        # print(d)
                        lines = json.dumps(d)
                        print(lines)
                        print('here we are using json.load', json.loads(lines))
        
        # if content_type == 'application/json':
        # # get lines inside the csv
        #     global lines 
        #     lines =response['Body'].read().decode('utf')
        #     # lines = json.dumps(lines)
        #     lines = json.loads(lines)
        #     print(type(lines))
        # return lines['Mga']
        
    except Exception as e:
        print(e)
        print('Error getting object {} from bucket {}. Make sure they exist and your bucket is in the same region as this function.'.format(key, bucket))
        raise e
              