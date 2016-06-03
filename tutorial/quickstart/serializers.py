from rest_framework import serializers
from quickstart.models import ImageUpload


class ImageUploadSerializer(serializers.HyperlinkedModelSerializer):
    imagefile_url = serializers.HyperlinkedIdentityField(view_name='imageupload-imagefile', read_only=True)
    
    class Meta:
        model = ImageUpload
        fields = ('url', 'pk', 'title', 'imagefile', 'imagefile_url')
        