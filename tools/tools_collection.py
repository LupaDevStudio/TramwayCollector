"""
Module tools of Tramway Collector
"""

###############
### Imports ###
###############


import random
import os
from typing import (
    List,
    Literal,
    Union
)

from tools.tools import (
    EMPTY_IMAGE_SOURCE,
    DICT_BADGES_IMAGES,
    PATH_COLLECTION,
    PATH_TRAMWAY_IMAGES,
    PATH_TEMP_FOLDER,
    load_json_file,
    save_json_file,
    check_if_name_exists,
    extract_filename_from_path
)

from tools.tools_image import (
    delete_stored_image
)

###############
### Classes ###
###############


class TramwayImage():
    """
    Class representing the image of a tramway

    ...

    Attributes
    ----------
    source : str
        the path of the image
    side : str
        the side of the tramway: it may take "left" or "right" as values
    category : str
        the category of the image: it may take "gold", "silver" or "bronze" as values
    default : bool
        boolean according to which the image as been defined as the default image of the gallery
    plus_plus : bool
        boolean according to which the image is a favorite one <3

    Methods
    -------
    get_default_badge()
        get the image if the badge associated to the default attribute
    get_plus_plus_badge()
        get the image if the badge associated to the plus_plus attribute
    """

    def __init__(self, source=EMPTY_IMAGE_SOURCE, side: Union[Literal["left", "right"], None] = None, category=None, default=True, plus_plus=False) -> None:
        self.source = source
        self.side = side
        self.category = category
        self.default = default
        self.plus_plus = plus_plus

    def get_default_badge(self):
        if self.default:
            return DICT_BADGES_IMAGES["default"][0]
        return DICT_BADGES_IMAGES["default"][1]

    def get_plus_plus_badge(self):
        if self.plus_plus:
            return DICT_BADGES_IMAGES["plus_plus"][0]
        return DICT_BADGES_IMAGES["plus_plus"][1]

    def __str__(self) -> str:
        string_repr = """
        {
            'source': '%s',
            'side': '%s',
            'category': '%s',
            'default': %s,
            'plus_plus': %s,
        }""" % (self.source, self.side, self.category, self.default, self.plus_plus)
        return string_repr


class Gallery():
    def __init__(self, name="", list_images=[]) -> None:
        self.name = name
        self.list_images: List[TramwayImage] = list_images

    def add_image(self, tramway_image: TramwayImage):
        self.list_images.append(tramway_image)

    def delete_image(self, tramway_image: TramwayImage):
        self.list_images.remove(tramway_image)

    def check_is_empty(self):
        return (len(self.list_images) == 0)

    def get_list_side_images(self, side):
        list_side_images = []
        for tramway_image in self.list_images:
            if tramway_image.side == side:
                list_side_images.append(tramway_image)
        return list_side_images

    def get_default_image(self, side) -> TramwayImage:
        list_side_images = self.get_list_side_images(side)
        for tramway_image in list_side_images:
            if tramway_image.default:
                return tramway_image
        empty_image = TramwayImage(side=side)
        return empty_image

    def update_default_image(self, tramway_image: TramwayImage):
        image: TramwayImage
        for image in self.get_list_side_images(side=tramway_image.side):
            image.default = False
        tramway_image.default = True

    def assign_default_image(self):
        for side in ["left", "right"]:
            default_image = self.get_default_image(side=side)
            if default_image.source == EMPTY_IMAGE_SOURCE:
                self.set_new_random_default(side=side)

    def set_new_random_default(self, side):
        """
        Set a new image as default in the corresponding side.

        Parameters
        ----------
        side : str
            side of the tramway

        Returns
        -------
        None
        """

        best_category, list_best_images = self.get_best_category(side=side)
        best_image = random.choice(list_best_images)
        best_image.default = True

    def get_best_category(self, side=None):
        """
        Determine the best category in the gallery and a random image with this category.

        Parameters
        ----------
        side : str, optional
            side of the tramway (default is None)

        Returns
        -------
        Literal["gold", "silver", "bronze"] | None
            the name of the best category
        List[TramwayImage]
            the list of images with the best categories
        """

        # Use integers to ease the comparison
        best_category = 0
        dict_categories = {
            "gold": 3,
            "silver": 2,
            "bronze": 1
        }
        dict_categories_reverse = {
            dict_categories[key]: key for key in (list(dict_categories.keys()))}
        list_images = self.list_images
        if side is not None:
            list_images = self.get_list_side_images(side)
        for tramway_image in list_images:
            if best_category < dict_categories[tramway_image.category]:
                best_category = dict_categories[tramway_image.category]
        if best_category != 0:
            list_best_images = [
                e for e in list_images if e.category == dict_categories_reverse[best_category]]
            return dict_categories_reverse[best_category], list_best_images
        return None, [TramwayImage()]

    def get_random_image(self):
        best_category, list_best_images = self.get_best_category()
        return (random.choice(list_best_images))

    def __str__(self) -> str:
        string_repr = f"'{self.name}': ["
        for image in self.list_images:
            string_repr += str(image) + ","
        string_repr = string_repr[:-1] + "]"
        return string_repr


class Collection():
    def __init__(self, list_galleries=[]) -> None:
        self.list_galleries: List[Gallery] = list_galleries

    def add_gallery(self, gallery: Gallery):
        # Check that the name doesn't already exist
        check_if_name_exists(self.list_galleries, gallery.name)
        self.list_galleries.append(gallery)

    def get_gallery(self, gallery_name: str):
        for gallery in self.list_galleries:
            if gallery_name == gallery.name:
                return gallery
        raise ValueError("The gallery under this name does not exist.")

    def change_name_gallery(self, my_gallery: Gallery, new_name):
        if my_gallery.name != new_name:
            check_if_name_exists(list_galleries=self.list_galleries,
                                 new_name=new_name)
            my_gallery.name = new_name
            return True
        return False

    def delete_gallery(self, gallery: Gallery):
        self.list_galleries.remove(gallery)

    def get_simple_collection(self) -> list:
        simple_collection = []
        for gallery in self.list_galleries:
            tramway_image: TramwayImage = gallery.get_random_image()
            simple_collection.append({
                "name": gallery.name,
                "image": tramway_image.source
            })
        return simple_collection

    def get_statistics_side(self, side, list_categories=["gold", "silver", "bronze"]):
        statistics = 0
        for gallery in self.list_galleries:
            best_category, list_best_images = gallery.get_best_category(side)
            if best_category in list_categories:
                statistics += 1
        return statistics

    def get_statistics(self):
        dict_statistics = {}
        dict_statistics["total"] = len(self.list_galleries)
        dict_statistics["total_sides"] = [
            self.get_statistics_side("left"),
            self.get_statistics_side("right")
        ]
        dict_statistics["gold"] = [
            self.get_statistics_side("left", ["gold"]),
            self.get_statistics_side("right", ["gold"])
        ]
        dict_statistics["silver"] = [
            self.get_statistics_side("left", ["silver"]),
            self.get_statistics_side("right", ["silver"])
        ]
        dict_statistics["bronze"] = [
            self.get_statistics_side("left", ["bronze"]),
            self.get_statistics_side("right", ["bronze"])
        ]
        return dict_statistics

    def __str__(self) -> str:
        string_repr = "[\n"
        for gallery in self.list_galleries:
            string_repr += "    " + str(gallery) + ",\n"
        string_repr = string_repr[:-3] + "\n]"
        return string_repr


#################
### Functions ###
#################


def init_collection_image_folder():
    """
    Create the json file for the collection and the folder for the images.
    This is done only when they do not exist.

    Parameters
    ----------
    None

    Returns
    -------
    None
    """

    # Folder for tramway images
    if not os.path.exists(PATH_TRAMWAY_IMAGES):
        os.mkdir(path=PATH_TRAMWAY_IMAGES)

    # Folder for temp image
    if not os.path.exists(PATH_TEMP_FOLDER):
        os.mkdir(path=PATH_TEMP_FOLDER)

    # Json file of the collection
    collection_file = "collection.json"
    if collection_file not in os.listdir(PATH_TRAMWAY_IMAGES):
        save_json_file(
            file_path=PATH_TRAMWAY_IMAGES + collection_file,
            dict_to_save={}
        )


def update_collection():
    """
    Update the collection  with the one contained in the json file.

    Parameters
    ----------
    None

    Returns
    -------
    None
    """

    # Open the json file of the collection
    dict_collection = load_json_file(
        file_path=PATH_COLLECTION
    )

    # Create the list of galleries, of type Gallery
    list_galleries = []
    for gallery_name in dict_collection:

        # Create the list of images, of type TramwayImage
        list_images = []
        for dict_image in dict_collection[gallery_name]:
            image = TramwayImage(
                source=PATH_TRAMWAY_IMAGES + dict_image["source"],
                side=dict_image["side"],
                category=dict_image["category"],
                default=dict_image["default"],
                plus_plus=dict_image["plus_plus"]
            )
            list_images.append(image)

        # Create the gallery
        gallery = Gallery(
            name=gallery_name,
            list_images=list_images
        )
        list_galleries.append(gallery)

    my_collection.list_galleries = list_galleries


def save_collection():
    """
    Save the collection in the corresponding json file.

    Parameters
    ----------
    None

    Returns
    -------
    None
    """

    dict_collection = {}
    gallery: Gallery
    for gallery in my_collection.list_galleries:
        list_dict_images = []
        tramway_image: TramwayImage
        for tramway_image in gallery.list_images:
            dict_image = {}
            dict_image["source"] = os.path.basename(tramway_image.source)
            dict_image["side"] = tramway_image.side
            dict_image["category"] = tramway_image.category
            dict_image["default"] = tramway_image.default
            dict_image["plus_plus"] = tramway_image.plus_plus
            list_dict_images.append(dict_image)
        dict_collection[gallery.name] = list_dict_images

    # Save in the json file of the collection
    save_json_file(
        file_path=PATH_COLLECTION,
        dict_to_save=dict_collection
    )


def clean_unused_images():
    stored_images_list = os.listdir(PATH_TRAMWAY_IMAGES)
    saved_images_list = []
    for gallery_list in my_collection.list_galleries:
        gallery_images_list = gallery_list.get_list_side_images(
            "left") + gallery_list.get_list_side_images("right")
        for image_dict in gallery_images_list:
            image_name = extract_filename_from_path(
                image_dict.source, with_extension=True)
            saved_images_list.append(image_name)
    for image_name in stored_images_list:
        if image_name.endswith("json"):
            continue
        if not image_name in saved_images_list:
            delete_stored_image(image_name.split(".")[0])


###############
### Process ###
###############


# Init the load of the collection
init_collection_image_folder()
my_collection = Collection(list_galleries=[])
update_collection()
