from django.conf import settings
from django.db import models
from .backend import Storage


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return '{0}/{1}'.format(instance.userid, filename)


class Files(models.Model):
    '''Files table definition'''
    userid = models.CharField(max_length=36, db_index=True)
    upload_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now_add=True)
    file = models.FileField(storage=Storage(), upload_to=user_directory_path)
    description = models.TextField()

    @property
    def name(self):
        return self.file.name.split('/')[-1]
    
    @property
    def path(self):
        return self.file.name.split('/')[0]
