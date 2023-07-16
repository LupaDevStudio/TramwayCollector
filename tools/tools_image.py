###############
### Imports ###
###############

### Python imports ###

import os
import shutil
import random
from PIL import Image as PIL_Image

### Module imports ###

from tools.tools import (
    PATH_TEMP_IMAGE,
    PATH_TRAMWAY_IMAGES,
    extract_filename_from_path
)

#################
### Constants ###
#################

IMAGE_BASE_SIZE = (500, 500)
IMAGE_EXT = ".jpg"

#################
### Functions ###
#################


def open_image(path: str) -> PIL_Image:
    return PIL_Image.open(path)


def crop_image_to_square(image: PIL_Image.Image) -> PIL_Image.Image:
    width, height = image.size
    smallest_dim = min(width, height)

    h_rest = width - smallest_dim
    h_offset = h_rest // 2

    v_rest = height - smallest_dim
    v_offset = v_rest // 2

    image = image.crop((h_offset,
                        v_offset,
                        h_offset + smallest_dim,
                        v_offset + smallest_dim))

    image = image.resize(
        IMAGE_BASE_SIZE,
        resample=PIL_Image.LANCZOS)

    return image


def save_temp_image(image: PIL_Image.Image) -> None:
    image = image.convert(mode="RGB")
    image.save(PATH_TEMP_IMAGE, optimize=True, quality=90)


def save_image(image: PIL_Image.Image, name: str) -> None:
    image.save(PATH_TRAMWAY_IMAGES + name + IMAGE_EXT)


def copy_as_square(input_path: str, temp=False) -> str:
    image = open_image(input_path)
    image = crop_image_to_square(image)
    image_name = extract_filename_from_path(input_path)
    if temp:
        save_temp_image(image)
    else:
        save_image(image=image,
                   name=image_name)
        return image_name + IMAGE_EXT


def transfer_temp_image(new_image_name: str) -> None:
    shutil.copy(PATH_TEMP_IMAGE, PATH_TRAMWAY_IMAGES +
                new_image_name + IMAGE_EXT)


def create_new_image_name():
    image_names = os.listdir(PATH_TRAMWAY_IMAGES)
    new_name = str(random.randint(0, 1e9))
    while new_name + IMAGE_EXT in image_names:
        new_name = str(random.randint(0, 1e9))
    return new_name


def delete_stored_image(image_name):
    os.remove(PATH_TRAMWAY_IMAGES + image_name + IMAGE_EXT)


def compress_images_in_folder(folder_path):
    images_list = os.listdir(folder_path)
    for image_name in images_list:
        image = open_image(folder_path + image_name)
        # os.remove(folder_path + image_name)
        image = crop_image_to_square(image)
        image.save(folder_path + image_name.replace(".png", ".jpg"))
