from django.db import models

class ImageUpload(models.Model):
    title = models.CharField(max_length=100)
    imagefile = models.FileField()