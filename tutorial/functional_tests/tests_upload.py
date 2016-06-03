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