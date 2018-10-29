from django.conf import settings
import boto3
import base64
from botocore.exceptions import ClientError
import json
from jose import jwt
import os

cognito_url = "https://easystore.auth.us-west-2.amazoncognito.com"
app_id = os.getenv("APP_ID")

def get_redirect_url(app_id, base_url, uri):
    cognito_redirect = "{url}/login?response_type=token&client_id={_id}&"\
                       "redirect_uri={burl}&state={uri}".format(url=cognito_url,
                                                                _id=app_id,
                                                                burl=base_url,
                                                                uri=uri)
    return cognito_redirect

def get_db_secret():

    secret_name = "easystore-db"
    region_name = "us-west-1"

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    secret = None
    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        if e.response['Error']['Code'] == 'DecryptionFailureException':
            # Secrets Manager can't decrypt the protected secret text using the provided KMS key.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response['Error']['Code'] == 'InternalServiceErrorException':
            # An error occurred on the server side.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response['Error']['Code'] == 'InvalidParameterException':
            # You provided an invalid value for a parameter.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response['Error']['Code'] == 'InvalidRequestException':
            # You provided a parameter value that is not valid for the current state of the resource.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response['Error']['Code'] == 'ResourceNotFoundException':
            # We can't find the resource that you asked for.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
    else:
        # Decrypts secret using the associated KMS CMK.
        # Depending on whether the secret is a string or binary, one of these fields will be populated.
        if 'SecretString' in get_secret_value_response:
            secret = json.loads(get_secret_value_response['SecretString'])
        else:
            decoded_binary_secret = base64.b64decode(get_secret_value_response['SecretBinary'])
            return decoded_binary_secret

    return secret

def get_cognito_user_details(session):
    return jwt.get_unverified_claims(session['ACCESS_TOKEN'])