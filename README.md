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

