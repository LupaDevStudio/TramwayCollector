"""
Test module of tools_collection
"""


###############
### Imports ###
###############


### Python imports ###

import sys

sys.path.append(".")

### Module imports ###

from tools.tools import (
    PATH_APP_IMAGES,
    EMPTY_IMAGE_SOURCE
)
from tools.tools_collection import (
    TramwayImage,
    Gallery,
    Collection
)


############################
### Test for the classes ###
############################


def test_collection():
    ### Test functions for the TramwayImage class ###
    my_tramway_left_1 = TramwayImage(
        source="test/test_data/tramway_image_left.png",
        side="left",
        category="gold",
        default=True,
        plus_plus=True
    )
    my_tramway_left_2 = TramwayImage(
        source="test/test_data/tramway_image_left.png",
        side="left",
        category="silver",
        default=False,
        plus_plus=False
    )
    my_tramway_left_3 = TramwayImage(
        source="test/test_data/tramway_image_left.png",
        side="left",
        category="gold",
        default=False,
        plus_plus=False
    )
    my_tramway_right_1 = TramwayImage(
        source="test/test_data/tramway_image_right.png",
        side="right",
        category="bronze",
        default=True,
        plus_plus=False
    )

    assert my_tramway_left_1.get_default_badge() == PATH_APP_IMAGES + "default.png"
    assert my_tramway_left_2.get_default_badge() == PATH_APP_IMAGES + \
        "default_off.png"
    assert my_tramway_left_1.get_plus_plus_badge() == PATH_APP_IMAGES + \
        "plus_plus.png"
    assert my_tramway_left_2.get_plus_plus_badge() == PATH_APP_IMAGES + \
        "plus_plus_off.png"

    ### Test functions for the Gallery class ###
    my_gallery_1 = Gallery(
        name="my_gallery_1",
        list_images=[]
    )

    my_gallery_1.add_image(my_tramway_left_1)
    assert len(my_gallery_1.list_images) == 1
    assert my_gallery_1.check_is_empty() == False
    my_gallery_1.delete_image(my_tramway_left_1)
    assert len(my_gallery_1.list_images) == 0
    assert my_gallery_1.check_is_empty() == True

    my_gallery_1.add_image(my_tramway_left_1)
    my_gallery_1.add_image(my_tramway_left_2)
    my_gallery_1.add_image(my_tramway_right_1)
    assert my_gallery_1.get_list_side_images("left") == [
        my_tramway_left_1, my_tramway_left_2]
    assert my_gallery_1.get_list_side_images("right") == [
        my_tramway_right_1]
    my_gallery_1.delete_image(my_tramway_right_1)
    assert my_gallery_1.get_list_side_images("right") == []

    assert my_gallery_1.get_default_image("left") == my_tramway_left_1
    assert my_gallery_1.get_default_image("right").source == EMPTY_IMAGE_SOURCE

    my_gallery_1.update_default_image(my_tramway_left_2)
    assert my_gallery_1.get_default_image("left") == my_tramway_left_2

    my_tramway_left_2.default = False
    my_gallery_1.assign_default_image()
    new_default = my_gallery_1.get_default_image("left")
    assert new_default in [my_tramway_left_1, my_tramway_left_2]
    my_gallery_1.assign_default_image()
    assert my_gallery_1.get_default_image("left") == new_default
    my_gallery_1.update_default_image(my_tramway_left_1)

    my_gallery_1.get_best_category()[0] == "gold"
    my_gallery_1.get_best_category("left")[0] == "gold"
    my_gallery_1.get_best_category("right")[0] == None
    my_gallery_1.delete_image(my_tramway_left_1)
    my_gallery_1.get_best_category("left")[0] == "silver"

    my_gallery_1.add_image(my_tramway_left_1)
    my_gallery_1.add_image(my_tramway_left_3)
    assert my_gallery_1.get_random_image() in [
        my_tramway_left_1, my_tramway_left_3]
    my_gallery_1.delete_image(my_tramway_left_2)

    my_gallery_2 = Gallery(
        name="my_gallery_2",
        list_images=[my_tramway_left_3, my_tramway_right_1]
    )
    my_gallery_2.assign_default_image()
    assert my_tramway_left_3.default == True
    assert my_tramway_right_1.default == True

    ### Test functions for the Collection class ###
    my_collection = Collection(
        list_galleries=[my_gallery_1]
    )
    assert len(my_collection.list_galleries) == 1
    my_collection.add_gallery(my_gallery_2)
    assert len(my_collection.list_galleries) == 2

    my_collection.get_gallery("my_gallery_1") == my_gallery_1
    try:
        my_collection.get_gallery("my_unknown_gallery")
        assert False
    except ValueError:
        assert True

    assert my_collection.change_name_gallery(
        my_gallery=my_gallery_1,
        new_name="my_new_gallery"
    )
    assert my_gallery_1.name == "my_new_gallery"
    assert False == my_collection.change_name_gallery(
        my_gallery=my_gallery_1,
        new_name="my_new_gallery"
    )

    my_collection.delete_gallery(my_gallery_2)
    assert len(my_collection.list_galleries) == 1
    my_collection.add_gallery(my_gallery_2)

    assert my_collection.get_simple_collection() == [
        {
            "name": "my_new_gallery",
            "image": my_tramway_left_1.source
        },
        {
            "name": "my_gallery_2",
            "image": my_tramway_left_3.source
        }
    ]

    assert my_collection.get_statistics() == {
        "total": 2,
        "total_sides": [2, 1],
        "gold": [2, 0],
        "silver": [0, 0],
        "bronze": [0, 1]
    }

    print(my_collection)
