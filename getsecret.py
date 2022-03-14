import boto3
import base64
from botocore.exceptions import ClientError
import json

def get_secret(id):
    region = 'us-east-1'
    print("Secrets Manager Region: "+region)

    client = boto3.session.Session().client(service_name='secretsmanager', region_name=region)

    try:
        resp = client.get_secret_value(SecretId=id)
        # Decrypts secret using the associated KMS CMK.
        # Depending on whether the secret is a string or binary, one of these fields will be populated.
        if 'SecretString' in resp:
            print("Found Secret String")
            return resp['SecretString']
        else:
            print("Found Binary Secret")
            return base64.b64decode(resp['SecretBinary'])
    except ClientError as err:
        print('Error Talking to SecretsManager: ' + err.response['Error']['Code'] + ', Message: ' + str(err))
        return None