###############
### Imports ###
###############

import os
import sys

sys.path.append(".")

from tools.tools_image import (
    PATH_TEMP_IMAGE,
    open_image,
    crop_image_to_square,
    save_temp_image,
    save_image
)

#############
### Tests ###
#############

image_path = "./test/test_data/test_image.jpg"

### Test open image ###

def test_open_image():
    image = open_image(image_path)
    # image.show()  # Uncomment to show the image


test_open_image()

### Test crop image to square ###

def test_crop_image_to_square():
    image = open_image(image_path)
    image = crop_image_to_square(image)
    # image.show()  # Uncomment to show the image


test_crop_image_to_square()

### Test save temp image ###

def test_save_temp_image():
    image = open_image(image_path)
    if os.path.exists(PATH_TEMP_IMAGE):
        os.remove(PATH_TEMP_IMAGE)
    save_temp_image(image)


test_save_temp_image()

### Test save image ###

def test_save_image():
    image = open_image(image_path)
    save_image(image=image,
               name="test_image")


test_save_image()
