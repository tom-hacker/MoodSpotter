import requests
from requests import ConnectionError
import json
from FaceMood import FaceMood

try:
    from types import SimpleNamespace as Namespace
except ImportError:
    from argparse import Namespace

url = "https://westcentralus.api.cognitive.microsoft.com/face/v1.0/detect"
params = {'returnFaceId': 'true',
          'returnFaceAttributes': 'age,gender,headPose,smile,facialHair,glasses,emotion,hair,makeup,occlusion,accessories,blur,exposure,noise'}
headers = {'Content-Type': 'application/octet-stream', 'Ocp-Apim-Subscription-Key': '1c607603f06646f6befb6cf1a4754a8d'}


class MoodDetector:

    def __init__(self):
        pass

    currentMood = FaceMood()

    def ms_get_image_data(self, byteImage):
        try:
            r = requests.post(url, params=params, headers=headers, data=byteImage)
            faces = json.loads(r.text, object_hook=lambda d: Namespace(**d))

            if r.status_code == 200 and len(faces) > 0:
                self.currentMood.divide_all_by(2)  # decrease importance of previous mood
                for face in faces:
                    evaluate_face(face, self.currentMood)
                self.currentMood.divide_all_by(len(faces))
                print(self.currentMood)
            else:
                print("Error code ", r.status_code)
                # TODO handle error codes

        except ConnectionError:
            # TODO connection didn't work
            print("connection error")


def evaluate_face(face, currentMood):
    facemood = face.faceAttributes.emotion
    print(facemood)
    currentMood.anger += facemood.anger
    currentMood.contempt += facemood.contempt
    currentMood.disgust += facemood.disgust
    currentMood.fear += facemood.fear
    currentMood.happiness += facemood.happiness
    currentMood.neutral += facemood.neutral
