import MoodCamera

directory = "/home/pi/Desktop/images"
print("Moodspotter is now running")

cameraExists = MoodCamera.take_photo("directory")


def main_loop():
    while True:
        MoodCamera.take_photo(directory)


def fallback_existing_image():
    img_bytes = MoodCamera.get_image_bytes(directory)
    if img_bytes:
        print("Using existing image")
        # TODO
    else:
        print("No existing image. Stopping immediately.")


# endless loop if camera is installed
if cameraExists:
    main_loop()
else:
    fallback_existing_image()






