"""
Module tools of Tramway Collector
"""

###############
### Imports ###
###############


import os
import json
from time import sleep
from kivy import platform


#################
### Constants ###
#################


### Version ###

__version__ = "1.0.3"

### Mode ###

if platform == "android":
    MOBILE_MODE = True
else:
    MOBILE_MODE = False


### Paths ###

PATH_DATA_FOLDER = "data/"
if MOBILE_MODE:
    from android.permissions import request_permissions, Permission, check_permission  # pylint: disable=import-error # type: ignore
    from android.storage import app_storage_path  # pylint: disable=import-error # type: ignore
    request_permissions([Permission.READ_EXTERNAL_STORAGE,
                        Permission.WRITE_EXTERNAL_STORAGE])
    PATH_DATA_APP_FOLDER = app_storage_path() + \
        "/" + ".tramwaycollector/"
    if not os.path.exists(PATH_DATA_APP_FOLDER):
        os.mkdir(PATH_DATA_APP_FOLDER)
else:
    PATH_DATA_APP_FOLDER = PATH_DATA_FOLDER
APPLICATION_NAME = "tramway-collector/"
PATH_TEMP_FOLDER = PATH_DATA_APP_FOLDER + "temp/"
PATH_TEMP_IMAGE = PATH_TEMP_FOLDER + "temp_image.jpg"
PATH_RESOURCES_FOLDER = "resources/"
PATH_TUTORIAL_IMAGES = PATH_RESOURCES_FOLDER + "tutorial/"
PATH_SETTINGS = PATH_DATA_APP_FOLDER + "settings.json"
if MOBILE_MODE and not os.path.exists(PATH_SETTINGS):
    with open(PATH_SETTINGS, "w") as file:
        json.dump({"language": "english", "default_path_images": app_storage_path()},
                  file)
PATH_LANGUAGE = PATH_RESOURCES_FOLDER + "languages/"
PATH_COLLECTION = PATH_DATA_APP_FOLDER + "collection/collection.json"
PATH_TRAMWAY_IMAGES = PATH_DATA_APP_FOLDER + "collection/"
PATH_APP_IMAGES = PATH_RESOURCES_FOLDER + "images_application/"
PATH_KIVY_FOLDER = PATH_RESOURCES_FOLDER + "kivy/"
ADD_IMAGE_SOURCE = PATH_APP_IMAGES + "add_image.png"
FRAME_IMAGE_SOURCE = PATH_APP_IMAGES + "frame_image.png"
FRAME_DEFAULT_IMAGE_SOURCE = PATH_APP_IMAGES + "frame_default_image.png"
EMPTY_IMAGE_SOURCE = PATH_RESOURCES_FOLDER + "logo_1024.png"
BLANK_IMAGE_SOURCE = ""

# Font path
DICT_LANGUAGE_FONT = {
    "french": "Roboto",
    "english": "Roboto",
    "german": "Roboto",
    "italian": "Roboto",
    "spanish": "Roboto",
    "japanese": "resources/fonts/ShinGoPr5.otf"
}

DICT_LANGUAGE_IMAGES_TUTORIAL = {
    "french": "french",
    "english": "english",
    "german": "english",
    "italian": "english",
    "spanish": "english",
    "japanese": "english"
}

# Extensions for the file chooser
ALLOWED_PICTURES_EXTENSIONS = [".png", ".jpg", ".jpeg"]

### Global variables ###

DICT_CATEGORY_IMAGES = {
    "gold": PATH_APP_IMAGES + "gold.png",
    "silver": PATH_APP_IMAGES + "silver.png",
    "bronze": PATH_APP_IMAGES + "bronze.png",
    "none": ADD_IMAGE_SOURCE
}

DICT_BADGES_IMAGES = {
    "plus_plus": [
        PATH_APP_IMAGES + "plus_plus.png",
        PATH_APP_IMAGES + "plus_plus_off.png"
    ],
    "default": [
        PATH_APP_IMAGES + "default.png",
        PATH_APP_IMAGES + "default_off.png"
    ]
}

DICT_LANGUAGE_CORRESPONDANCE = {
    "french": "Français",
    "english": "English",
    "german": "Deutsch",
    "italian": "Italiano",
    "spanish": "Español",
    "japanese": "Japanese"
}


#################
### Functions ###
#################


### Path manipulation ###

def extract_filename_from_path(path, with_extension=False):
    '''
    Return the filename inside a path.

    Parameters
    ----------
    path : str
        Path of the file.

    Returns
    -------
    str
        Name of the file
    '''
    filename_with_ext = os.path.basename(path)
    if with_extension:
        return filename_with_ext
    else:
        inv_filename_with_ext = filename_with_ext[::-1]
        inv_filename = inv_filename_with_ext.split('.', 1)[1]
        filename = inv_filename[::-1]
        return filename


def extract_foldername_from_path(path):
    '''
    Return the foldername of a path.

    Parameters
    ----------
    path : str
        Path of the file.

    Returns
    -------
    str
        Name of the folder
    '''
    return os.path.dirname(path)


def crop_path(path):
    """
    Takes the local path of the image.
    It removes the beginning of the path dependant of the computer.

    Parameters
    ----------
    path : str
        Path to crop

    Returns
    -------
    str
        The path cropped
    """

    if APPLICATION_NAME in path:
        return (path.split(APPLICATION_NAME, 2)[1])
    return path


def load_json_file(file_path: str) -> dict:
    """
    Load a json file, according the specified path.

    Parameters
    ----------
    file_path : str
        Path of the json file.

    Returns
    -------
    dict
        Content of the json file
    """
    with open(file_path, "r", encoding="utf-8") as file:
        res = json.load(file)
    return res


def save_json_file(file_path: str, dict_to_save: dict) -> None:
    """
    Save the content of the given dictionnary inside the 
    specified json file.

    Parameters
    ----------
    file_path : str
        Path of the json file.

    dict_to_save : dict
        Dictionnary to save

    Returns
    -------
    None
    """
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(dict_to_save, file)


def detect_single_multiple_galleries(number):
    dict_language_statistics = my_language.dict_language["settings"]["statistics"]
    if number > 1:
        return dict_language_statistics["galleries"]
    return dict_language_statistics["gallery"]


def check_if_name_exists(list_galleries, new_name):
    for gallery in list_galleries:
        if gallery.name == new_name:
            raise ValueError()
    return True


################
### Settings ###
################


class Language():
    def __init__(self, code_language):
        self.code_language = code_language
        self.dict_language = {}
        self.dict_buttons = {}
        self.dict_messages = {}
        self.font = DICT_LANGUAGE_FONT[code_language]
        self.change_language()

    def convert_language_code(self, language):
        """
        Convert the language seen in the interface into its code.

        Parameter
        ---------
        language : str
            The language seen in the interface

        Return
        ------
        None        
        """
        for code_language in DICT_LANGUAGE_CORRESPONDANCE.keys():
            if language == DICT_LANGUAGE_CORRESPONDANCE[code_language]:
                self.code_language = code_language
                break

    def change_language(self):
        """
        Change the language of the interface.
        It updates the settings and saves the new dictionary.
        It also adapts the font depending on the language (for instance for Japanese).

        Parameter
        ---------
        None

        Return
        ------
        None        
        """
        update_settings("language", self.code_language)
        with open(PATH_LANGUAGE + self.code_language + ".json", "r", encoding="utf-8") as file:
            self.dict_language = json.load(file)
        self.dict_buttons = self.dict_language["generic"]["popup"]["dict_buttons"]
        self.dict_messages = self.dict_language["generic"]["popup"]["dict_messages"]
        self.font = DICT_LANGUAGE_FONT[self.code_language]


def update_settings(key, value):
    """
    Update a certain field in the dictionary of settings and save it.

    Parameters
    ----------
    key : str
        Key of the field to update

    value : str
        New value of the field

    Returns
    -------
    None
    """
    SETTINGS[key] = value
    save_json_file(PATH_SETTINGS, SETTINGS)


# Load the settings and the language
SETTINGS = load_json_file(PATH_SETTINGS)
my_language = Language(SETTINGS["language"])
