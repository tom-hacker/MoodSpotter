import MoodCamera
import MoodDetector
import SpotifyConnector

directory = "/home/pi/Desktop/images"
print("Moodspotter is now running")

cameraExists = MoodCamera.take_photo("directory")
moodDetector = MoodDetector.MoodDetector()
spotifyConnector = SpotifyConnector.SpotifyConnector()


def main_loop():
    while True:
        MoodCamera.take_photo(directory)


def fallback_existing_image():
    img_bytes = MoodCamera.get_image_bytes(directory)
    if img_bytes:
        print("Using existing image")
        moodDetector.ms_get_image_data(img_bytes)
    else:
        print("No existing image. Stopping immediately.")


# endless loop if camera is installed
if cameraExists:
    main_loop()
else:
    fallback_existing_image()






