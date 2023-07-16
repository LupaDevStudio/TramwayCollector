"""
Module to create components useful for the display of the other screens.
"""

###############
### Imports ###
###############

### Python imports ###
import os


### Kivy imports ###

from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.properties import StringProperty, ObjectProperty, ListProperty

### Module imports ###

from tools.tools_collection import (
    TramwayImage
)
from tools.tools import (
    DICT_CATEGORY_IMAGES,
    FRAME_IMAGE_SOURCE,
    FRAME_DEFAULT_IMAGE_SOURCE,
    SETTINGS,
    my_language,
    MOBILE_MODE
)
from tools.tools_kivy import (
    pink_color
)

if MOBILE_MODE:
    from android.storage import primary_external_storage_path  # pylint: disable=import-error # type: ignore
    PRIMARY_EXT_STORAGE = primary_external_storage_path()
else:
    PRIMARY_EXT_STORAGE = "/"


###############
### Classes ###
###############

class BadgedImage(RelativeLayout):
    """
    Class corresponding to the image with the badges and the button to edit it
    """

    def __init__(self, tramway_image: TramwayImage, **kw):
        super().__init__(**kw)
        self.tramway_image = tramway_image
        if tramway_image.default:
            frame_source = FRAME_DEFAULT_IMAGE_SOURCE
        else:
            frame_source = FRAME_IMAGE_SOURCE
        image = ImageWithFrame(
            size_hint=(1, 1),
            source=tramway_image.source,
            frame_source=frame_source,
            allow_stretch=True
        )
        self.add_widget(image)
        self.image_button = Button(
            size_hint=(1, 1),
            background_color=(0, 0, 0, 0)
        )
        self.add_widget(self.image_button)
        if tramway_image.plus_plus:
            # Plus plus badge
            plus_plus_image = Image(
                size_hint=(0.15, 0.15),
                pos_hint={"x": 0.1, "y": 0.12},
                source=tramway_image.get_plus_plus_badge(),
                allow_stretch=True
            )
            self.add_widget(plus_plus_image)
        # Category badge
        category_badge = Image(
            size_hint=(0.3, 0.3),
            pos_hint={"x": 0.8, "y": 0.75},
            source=DICT_CATEGORY_IMAGES[tramway_image.category],
            allow_stretch=True
        )
        self.add_widget(category_badge)

    def assign_function(self, function):
        """
        Assign a function to the button linked to the image.

        Parameters
        ----------
        function : function
            Function to assign to the click on the image.
        """
        self.image_button.on_release = function


class LoadDialog(FloatLayout):
    """
    Class to open a file chooser
    """

    def __init__(self, filters_list=None, **kwargs):
        super().__init__(**kwargs)
        self.update_path()
        if filters_list is None:
            filters_list = []
        self.filters_list = filters_list
        self.cancel_label = my_language.dict_language[
            "generic"]["file_chooser"]["cancel"]
        self.load_label = my_language.dict_language[
            "generic"]["file_chooser"]["load"]
        self.font = my_language.font

    font = StringProperty("Roboto")
    default_path = StringProperty("")
    filters_list = ListProperty([])
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)
    pink_color = pink_color
    cancel_label = StringProperty("")
    load_label = StringProperty("")

    def update_path(self):
        """
        Update the path to open the file explorer at the last known location.
        """
        if not os.path.exists(SETTINGS["default_path_images"]):
            SETTINGS["default_path_images"] = PRIMARY_EXT_STORAGE
        self.default_path = SETTINGS["default_path_images"]


####################
### Custom Image ###
####################


class ImageWithFrame(RelativeLayout):
    """
    Class to create kivy images with a frame attached.

    Two sources are specified, one for the image and one for the frame.
    """

    def __init__(self,
                 source=None,
                 frame_source=FRAME_IMAGE_SOURCE,
                 size_hint=(None, None),
                 allow_stretch=False,
                 **kwargs):
        super().__init__(size_hint=size_hint, **kwargs)
        self.image = Image(
            source=source,
            size_hint=(0.85, 0.85),
            pos_hint={"x": 0.075, "y": 0.075},
            allow_stretch=allow_stretch)
        self.add_widget(self.image)
        self.frame = Image(
            source=frame_source,
            allow_stretch=allow_stretch,
            size_hint=(1, 1))
        self.add_widget(self.frame)
