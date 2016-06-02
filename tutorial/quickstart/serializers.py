from rest_framework import serializers
from quickstart.models import ImageUpload


class ImageUploadSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ImageUpload
        fields = ('url', 'pk', 'title', 'imagefile')
        