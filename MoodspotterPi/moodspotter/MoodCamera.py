from picamera import PiCamera, PiCameraError
from time import sleep
import os


class MoodCamera:
    def __init__(self):
        pass

    imgName = "/image.jpg"
    directory = ""
    camera = ""
    def init_camera(self, dir):
        try:
            self.directory = dir
            self.camera = PiCamera()
            self.camera.rotation = 180
            return self.take_photo()
        except PiCameraError:
            print("Error when initializing camera!")
            return False


    def take_photo(self):
        if not os.path.exists(self.directory):
            os.makedirs(self.directory)
        try:
            self.camera.start_preview()
            sleep(5)
            self.camera.capture(self.directory + self.imgName)
            self.camera.stop_preview()
            return True
        except PiCameraError:
            print("There is no camera installed!")
            return False


    def get_image_bytes(self):
        if not os.path.exists(self.directory + self.imgName):
            return False
        img = open(self.directory + self.imgName, "rb")
        f = img.read()
        img.close()
        return f
