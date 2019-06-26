import requests
from requests import ConnectionError
import json
from FaceMood import FaceMood
from conf.Config import ms_cognitive_url, ms_cognitive_headers_byteimg, ms_cognitive_params
import ErrorHandler
try:
    from types import SimpleNamespace as Namespace
except ImportError:
    from argparse import Namespace


class MoodDetector:

    def __init__(self):
        pass

    currentMood = FaceMood()

    def ms_get_image_data(self, byteImage):
        try:
            r = requests.post(ms_cognitive_url,
                              params=ms_cognitive_params,
                              headers=ms_cognitive_headers_byteimg,
                              data=byteImage)
            faces = json.loads(r.text, object_hook=lambda d: Namespace(**d))

            if r.status_code == 200 and len(faces) > 0:
                self.currentMood.divide_all_by(2)  # decrease importance of previous mood
                for face in faces:
                    evaluate_face(face, self.currentMood)
                self.currentMood.divide_all_by(len(faces))
                print(self.currentMood)
                return True
            elif r.status_code == 200:
                print("No faces found")
                return False
            else:
                ErrorHandler.handle_error_response(r, "MS Cognitive Services")
                return False

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
