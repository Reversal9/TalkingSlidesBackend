from djongo.storage import GridFSStorage
from django.db import models
from django.conf import settings
from bson import ObjectId

grid_fs_storage = GridFSStorage(collection='myfiles', base_url='/media/myfiles/')

class Pdf(models.Model):
    id = models.BigAutoField(primary_key=True)
    file = models.FileField(upload_to='pdfs', storage=grid_fs_storage)
    file_id = models.CharField(max_length=24, unique=True)  # Store ObjectId as a string


class VideoMetadata(models.Model):
    id = models.BigAutoField(primary_key=True)
    file = models.FileField(upload_to='pdfs', storage=grid_fs_storage)
    title = models.CharField(max_length=255)
    upload_date = models.DateTimeField(auto_now_add=True)
    thumbnail = models.ImageField(upload_to="thumbnails/", null=True, blank=True)
    file_id = models.CharField(max_length=24, unique=True)  # Store ObjectId as a string

class Avatar(models.Model):
    id = models.BigAutoField(primary_key=True)
    upload_date = models.DateTimeField(auto_now_add=True)
    file = models.ImageField(upload_to="avatars/", null=True, blank=True)
    file_id = models.CharField(max_length=24, unique=True)  # Store ObjectId as a string
