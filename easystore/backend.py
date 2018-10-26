from boto3.exceptions import Boto3Error
from botocore.exceptions import ClientError
from django.conf import settings
from django_warrant.backend import CognitoBackend as Cognito,\
                                   CognitoUser



class CognitoBackend(Cognito):
    '''Extending CognitoBackend class to allow for registration'''

    def register(self, username,
                 password,
                 email,
                 first_name,
                 last_name):
        '''Register user

        :param username: Cognito Username
        :param password: Cognito Password
        :param email: Email
        :param first_name: First name
        :param last_name: Last name
        :returns: Response from Cognito
        '''
        cognito_user = CognitoUser(
            settings.COGNITO_USER_POOL_ID,
            settings.COGNITO_APP_ID,
            access_key=getattr(settings, 'AWS_ACCESS_KEY_ID', None),
            secret_key=getattr(settings, 'AWS_SECRET_ACCESS_KEY', None),
            username=username)

        try:
            cognito_user.add_base_attributes(**{'given_name': first_name,
                                                'family_name': last_name,
                                                'email': email})
            response = cognito_user.register(username, password)
        except (Boto3Error, ClientError) as e:
            return self.handle_error_response(e)

        return response

    def validate_user(self, confirmation_code, username):
        '''Validate user

        :param confirmation_code: Confirmation code received from Cognito
        :param username: Cognito Username
        '''
        cognito_user = CognitoUser(
            settings.COGNITO_USER_POOL_ID,
            settings.COGNITO_APP_ID,
            access_key=getattr(settings, 'AWS_ACCESS_KEY_ID', None),
            secret_key=getattr(settings, 'AWS_SECRET_ACCESS_KEY', None),
            username=username)
        cognito_user.confirm_sign_up(confirmation_code,
                                     username=username)