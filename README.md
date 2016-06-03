# Django-rest-framework Practice Project

## Project Start
```
>virtualenv virtualenv --python=f:\Anaconda3\python.exe
>virtualenv\Scripts\activate.bat
(virtualenv) >pip install django
(virtualenv) >pip install djangorestframework
(virtualenv) >django-admin.py startproject tutorial
(virtualenv) >cd tutorial
(virtualenv) tutorial>django-admin.py startapp quickstart
(virtualenv) tutorial>python manage.py migrate

>git init
>type .gitignore
*.pyc
/virtualenv
/tutorial/db.sqlite3
>git add -A
>git commit -m "project start"
```

## Django Rest Framework Start and ImageUpload Model Create
settings.py

```
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'quickstart',
    'rest_framework',
]

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': ('rest_framework.permissions.AllowAny',),
    'PAGE_SIZE': 10
}
```

models.py
```
class ImageUpload(models.Model):
    title = models.CharField(max_length=100)
    imagefile = models.FileField(null=True)
```

serializers.py
```
class ImageUploadSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ImageUpload
        fields = ('url', 'pk', 'title', 'imagefile')
```

views.py
```
class ImageUploadViewSet(viewsets.ModelViewSet):
    queryset = ImageUpload.objects.all()
    serializer_class = ImageUploadSerializer
```

urls.py
```
router = routers.DefaultRouter()
router.register(r'imageuploads', views.ImageUploadViewSet)

urlpatterns = [
    url(r'^', include(router.urls))
]
```

command
```
(virtualenv) tutorial>python manage.py makemigration
(virtualenv) tutorial>python manage.py migrate
(virtualenv) tutorial>python manage.py runserver
```

여기까지 진행하면 사이트에 접속해서 작동하는 모습을 볼 수 있다.

### 참고 링크
- http://www.django-rest-framework.org/tutorial/quickstart/

## 업로드 테스트
command
```
(virtualenv) tutorial>pip install requests
```

functional_tests/test_image.png 준비

functional_tests/tests_upload.py
```
from django.test import LiveServerTestCase
import requests

class UploadTest(LiveServerTestCase):
    def test_upload(self):
        file = open('functional_tests/test_image.png','rb')
        files = [
            ('imagefile', ('test_image.png', file, 'image/png'))
        ]
        r = requests.post(self.live_server_url + '/imageuploads/', 
            data={
                'title':'Test Image'
            }, 
            files=files
        )
        file.close()
        self.assertEqual(201, r.status_code)  # created
```
command
```
(virtualenv) tutorial>python manage.py test functional_tests
```
테스트 실행하면 업로드된 파일이 tutorial 폴더에 저장된것을 확인할 수 있다.

git tag upload_test

## 업로드시 파일 저장위치 변경
settings.py 에 다음을 추가합니다.
```
MEDIA_ROOT = os.path.abspath(os.path.join(BASE_DIR, '../uploadfiles'))
```
업로드 되는 파일이 프로젝트 루트 기준으로 /uploadfiles 가 됩니다.

models.py 에서 imagefile 에 upload_to 를 추가합니다. 
```
imagefile = models.FileField(upload_to='imagefile/%Y/%m/%d', null=True)
```
이 필드로 인해 업로드되는 파일은 /uploadfiles/imagefile/2016/06/02 형태가 됩니다.

functional_tests/tests_upload.py
```
from tutorial.settings import MEDIA_ROOT
import os

class UploadTest(LiveServerTestCase):
    def test_upload(self):
        # 기존 코드 이후에 추가
        imagefile = r.json()['imagefile']
        imagefilepath = imagefile.__str__().replace(self.live_server_url + '/imageuploads/','')
        imagefile_realpath = os.path.abspath(os.path.join(MEDIA_ROOT, imagefilepath))
        os.remove(imagefile_realpath)
```
업로드된 파일을 지우는 코드입니다.
파일이 없을 경우 os.remove(imagefile_realpath) 에서 에러가 발생합니다.

command
```
(virtualenv) tutorial>python manage.py test functional_tests
```
테스트를 돌려 확인해 봅니다.

## 다운로드 구현

serializers.py
```
class ImageUploadSerializer(serializers.HyperlinkedModelSerializer):
    imagefile_url = serializers.HyperlinkedIdentityField(view_name='imageupload-imagefile', read_only=True)
    
    class Meta:
        model = ImageUpload
        fields = ('url', 'pk', 'title', 'imagefile', 'imagefile_url')
```
views.py
```
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
```
tests_upload.py
test_upload 메소드 명을 test_upload_download 로 바꿈.
아래 내용 추가
```
import shutil
import filecmp

        # 파일의 마지막 부분을 아래와 같이 수정
        # --------------------------------
        # 다운로드 경로를 알아내고 요청을 보낸다.
        imagefile_url = r.json()['imagefile_url']
        r = requests.get(imagefile_url, stream=True)
        # 다운로드한 파일을 저장한다.
        with open('functional_tests/download.png', 'wb') as out_file:
            shutil.copyfileobj(r.raw, out_file)
        # 업로드 한 파일과 다운로드 한 파일이 같은지 비교한다.
        self.assertTrue(filecmp.cmp('functional_tests/test_image.png', 'functional_tests/download.png'))

        # 다운로드한 파일을 삭제한다.
        os.remove('functional_tests/download.png')
        # --------------------------------
        
        # 업로드된 파일을 지운다.
        imagefilepath = imagefile.__str__().replace(self.live_server_url + '/imageuploads/','')
        imagefile_realpath = os.path.abspath(os.path.join(MEDIA_ROOT, imagefilepath))
        os.remove(imagefile_realpath)
```