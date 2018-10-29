from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage
from boto.sdb.db import property


class Storage(S3Boto3Storage):
    
    location = settings.AWS_S3_LOCATION
    default_acl = 'private'
    file_overwrite = True
    custom_domain = False

        
        