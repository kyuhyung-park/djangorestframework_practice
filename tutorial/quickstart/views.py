from django.shortcuts import render
from rest_framework import viewsets

from quickstart.models import ImageUpload
from quickstart.serializers import ImageUploadSerializer

from rest_framework.decorators import detail_route
from django.http import FileResponse

class ImageUploadViewSet(viewsets.ModelViewSet):
    queryset = ImageUpload.objects.all()
    serializer_class = ImageUploadSerializer
    
    @detail_route(methods=['get'])
    def imagefile(self, request, pk=None):
        r = self.get_object()
        # 확장자 추출
        ext = '*'
        if r.imagefile.path:
            ext = r.imagefile.path.split('.')[-1]
        content_type = 'image/' + ext
        # 다운로드용 Response 반환
        response = FileResponse(open(r.imagefile.path, 'rb'), content_type=content_type)
        return response