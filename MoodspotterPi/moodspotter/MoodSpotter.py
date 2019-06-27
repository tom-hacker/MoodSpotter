import MoodCamera
import MoodDetector
import SpotifyConnector
from time import sleep

directory = "/home/pi/Desktop/images"
print("Moodspotter is now running")

camera = MoodCamera.MoodCamera()
cameraExists = camera.init_camera(directory)
moodDetector = MoodDetector.MoodDetector()
spotifyConnector = SpotifyConnector.SpotifyConnector()


def main_loop():
    while True:
        img_bytes = camera.get_image_bytes()
        if moodDetector.ms_get_image_data(img_bytes):
            spotifyConnector.browse_for_mood(moodDetector.currentMood)
            sleep(30)
        else:
            sleep(5)
        camera.take_photo()


def fallback_existing_image():
    img_bytes = camera.get_image_bytes()
    if img_bytes:
        print("Using existing image")
        moodDetector.ms_get_image_data(img_bytes)
        spotifyConnector.browse_for_mood(moodDetector.currentMood)
    else:
        print("No existing image. Stopping immediately.")


# endless loop if camera is installed
if cameraExists:
    main_loop()
else:
    fallback_existing_image()






