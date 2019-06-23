from picamera import PiCamera, PiCameraError
from time import sleep
import os

imgName = "/image.jpg"


def take_photo(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
    try:
        camera = PiCamera()
        camera.rotation = 180
        camera.start_preview()
        sleep(5)
        camera.capture(directory + imgName)
        camera.stop_preview()
        return True
    except PiCameraError:
        print("There is no camera installed!")
        return False


def get_image_bytes(directory):
    if not os.path.exists(directory + imgName):
        return False
    img = open(directory + imgName, "rb")
    f = img.read()
    b = bytearray(f)
    img.close()
    return b
