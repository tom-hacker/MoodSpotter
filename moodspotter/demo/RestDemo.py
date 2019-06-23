import requests
import json
url = "https://westcentralus.api.cognitive.microsoft.com/face/v1.0/detect"
#imgurl = 'https://i.imgur.com/bbSNgEP.jpg'
imgLocation = '/home/pi/Desktop/images/image.jpg'


params = {'returnFaceId': 'true',
          'returnFaceAttributes': 'age,gender,headPose,smile,facialHair,glasses,emotion,hair,makeup'}
headers = {'Content-Type': 'application/octet-stream', 'Ocp-Apim-Subscription-Key': '1c607603f06646f6befb6cf1a4754a8d'}

with open(imgLocation, "rb") as image:
    f = image.read()
    b = bytearray(f)
    r = requests.post(url, params=params, headers=headers, data=f)

print(r.url)
print(r.request)
print(r.status_code)
print(r.text)
