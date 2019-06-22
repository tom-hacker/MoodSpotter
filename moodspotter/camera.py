from picamera import PiCamera
from time import sleep
import os

directory = "/home/pi/Desktop/images"
if not os.path.exists(directory):
    os.makedirs(directory)

camera = PiCamera()

camera.rotation = 180
camera.start_preview()
sleep(5)
camera.capture("/home/pi/Desktop/images/image.jpg")
camera.stop_preview()