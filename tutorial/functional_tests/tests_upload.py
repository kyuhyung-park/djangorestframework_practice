from django.test import LiveServerTestCase
import requests
from tutorial.settings import MEDIA_ROOT
import os

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
        
        imagefile = r.json()['imagefile']
        imagefilepath = imagefile.__str__().replace(self.live_server_url + '/imageuploads/','')
        imagefile_realpath = os.path.abspath(os.path.join(MEDIA_ROOT, imagefilepath))
        os.remove(imagefile_realpath)
        
        