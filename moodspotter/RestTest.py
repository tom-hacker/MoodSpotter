import requests
import json
url = "https://westcentralus.api.cognitive.microsoft.com/face/v1.0/detect"
#url = "https://jsonplaceholder.typicode.com/todos/1"
imgurl = 'https://i.imgur.com/bbSNgEP.jpg'


params = {'returnFaceId': 'true',
          'returnFaceAttributes': 'age,gender,headPose,smile,facialHair,glasses,emotion,hair,makeup'}
payload = {'url': 'https://i.imgur.com/bbSNgEP.jpg'}
headers = {'Content-Type': 'application/json', 'Ocp-Apim-Subscription-Key': '1c607603f06646f6befb6cf1a4754a8d'}

r = requests.post(url, params=params, headers=headers, data=json.dumps(payload))

print(r.url)
print(r.request)
print(r.status_code)
print(r.text)
