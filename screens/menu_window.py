###############
### Imports ###
###############

### Python imports ###

from functools import partial

### Kivy imports ###

from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.properties import StringProperty

### Module imports ###

from screens.components import (
    ImageWithFrame
)
from tools.tools import (
    PATH_RESOURCES_FOLDER,
    ADD_IMAGE_SOURCE,
    FRAME_IMAGE_SOURCE,
    my_language
)
from tools.tools_kivy import (
    global_spacing,
    window_size,
    scale_image
)
from tools.tools_collection import (
    my_collection,
    Gallery
)

#################
### Main menu ###
#################


class MenuWindow(Screen):
    """
    Class displaying the main menu.
    """

    def __init__(self, **kw):
        super().__init__(**kw)

    font = StringProperty("Roboto")
    path_resources = PATH_RESOURCES_FOLDER
    number_cols = 3
    spacing = global_spacing["horizontal"]
    label_height = 40 * scale_image
    padding = [0.05 * window_size[0], 0, 0.05 * window_size[0], 0]

    def init_screen(self):
        self.ids.my_sv_layout.reset_screen()
        self.font = my_language.font
        self.build_scroll_view()

    def build_scroll_view(self):
        simple_collection = my_collection.get_simple_collection()
        image_dimension = (window_size[0] - 2 * self.padding[0] - self.spacing * (
            self.number_cols - 1)) / self.number_cols
        height_layout = image_dimension + self.label_height
        for dict_simple_gallery in simple_collection:
            relative_layout = RelativeLayout(
                size_hint=(None, None),
                height=height_layout,
                width=image_dimension
            )
            # Label for the name of the gallery
            name_label = Label(
                size_hint=(None, None),
                width=image_dimension,
                height=self.label_height,
                color=self.manager.color_label,
                text=dict_simple_gallery["name"],
                pos_hint={"x": 0, "y": 0},
                font_name=self.font
            )
            relative_layout.add_widget(name_label)
            # Image
            image = ImageWithFrame(
                size_hint=(None, None),
                width=image_dimension,
                height=image_dimension,
                source=dict_simple_gallery["image"],
                allow_stretch=True,
                y=self.label_height,
                frame_source=FRAME_IMAGE_SOURCE
            )
            relative_layout.add_widget(image)
            # Button to click on the image
            button = Button(
                size_hint=(None, None),
                width=image_dimension,
                height=image_dimension,
                background_color=(0, 0, 0, 0),
                y=self.label_height
            )
            button.on_release = partial(self.open_gallery, dict_simple_gallery)
            relative_layout.add_widget(button)
            self.ids.my_sv_layout.add_widget(relative_layout)

        # Add gallery
        relative_layout = RelativeLayout(
            size_hint=(None, None),
            height=height_layout,
            width=image_dimension
        )
        image = Image(
            size_hint_y=None,
            height=image_dimension / 1.5,
            pos_hint={"center_x": 0.5},
            y=image_dimension / 3 + self.label_height / 2,
            source=ADD_IMAGE_SOURCE,
            allow_stretch=True
        )
        relative_layout.add_widget(image)
        button = Button(
            size_hint=(None, None),
            height=image_dimension / 1.5,
            width=image_dimension / 1.5,
            pos_hint={"center_x": 0.5},
            y=image_dimension / 3 + self.label_height / 2,
            background_color=(0, 0, 0, 0)
        )
        button.on_release = self.add_gallery
        relative_layout.add_widget(button)
        self.ids.my_sv_layout.add_widget(relative_layout)

    def add_gallery(self):
        new_gallery = Gallery(name="", list_images=[])
        self.manager.init_screen("image_edition", gallery=new_gallery)

    def open_gallery(self, dict_simple_gallery):
        gallery = my_collection.get_gallery(dict_simple_gallery["name"])
        self.manager.init_screen("gallery", gallery=gallery)
