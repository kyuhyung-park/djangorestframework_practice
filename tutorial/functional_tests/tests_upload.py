from django.test import LiveServerTestCase
import requests
from tutorial.settings import MEDIA_ROOT
import os

import shutil
import filecmp

class UploadTest(LiveServerTestCase):
    def test_upload_download(self):
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

        imagefile = r.json()['imagefile']

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

    def test_upload_file(self):
        # title 만 입력하여 추가한다.
        r = requests.post(self.live_server_url + '/imageuploads/',
            data={
                'title':'Test Image'
            }
        )
        self.assertEqual(201, r.status_code)  # created
        url = r.json()['url']

        # /imageuploads/{pk}/upload 로 파일을 전송한다.
        file = open('functional_tests/test_image.png','rb')
        files = [
            ('imagefile', ('test_image.png', file, 'image/png'))
        ]
        r = requests.post(url + 'upload/',
            files=files
        )
        file.close()
        self.assertEqual(200, r.status_code)
        self.assertEqual('upload success', r.json()['status'])

        # 업로드된 파일을 지운다.
        r = requests.get(url)
        imagefile = r.json()['imagefile']
        imagefilepath = imagefile.__str__().replace(url,'')
        imagefile_realpath = os.path.abspath(os.path.join(MEDIA_ROOT, imagefilepath))
        os.remove(imagefile_realpath)

        # 파일없이 요청하면 400 코드를 반환한다.
        r = requests.post(url + 'upload/')
        self.assertEqual(400, r.status_code)
        self.assertEqual('no file', r.json()['status'])
