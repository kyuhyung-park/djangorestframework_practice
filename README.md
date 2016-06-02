# Django Django-rest-framework file upload download sample

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

##
- http://www.django-rest-framework.org/tutorial/quickstart/