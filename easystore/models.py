from django.db import models

class Files(models.Model):
    '''Files table definition'''
    userid = models.CharField(max_length=36, db_index=True)
    upload_time = models.DateTimeField(auto_now_add=True)
    filename = models.CharField(max_length=100)
    description = models.TextField()

