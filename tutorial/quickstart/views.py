from django.shortcuts import render
from rest_framework import viewsets

from quickstart.models import ImageUpload
from quickstart.serializers import ImageUploadSerializer

class ImageUploadViewSet(viewsets.ModelViewSet):
    queryset = ImageUpload.objects.all()
    serializer_class = ImageUploadSerializer
    