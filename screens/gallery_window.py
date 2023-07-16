"""
Module to define the Kivy content of the gallery screen.

Classes
-------
GalleryWindow : content of the gallery screen.
"""

###############
### Imports ###
###############


### Python imports ###

from functools import partial
from math import ceil

### Kivy imports ###

from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.properties import StringProperty

### Module imports ###

from tools.tools import (
    ADD_IMAGE_SOURCE,
    PATH_APP_IMAGES,
    DICT_CATEGORY_IMAGES,
    my_language
)
from tools.tools_kivy import (
    global_spacing,
    window_size,
    color_label,
    create_standard_popup,
    scale_image
)
from tools.tools_collection import (
    Gallery,
    save_collection
)
from screens.components import BadgedImage
from screens.collection_window import my_collection


####################
### Gallery menu ###
####################


class GalleryWindow(Screen):
    """
    Screen to display the gallery.

    Attributes
    ----------
    font : str
        Name of the font used to display the text.

    label_height : float
        Height of a label for the display.

    spacing : float
        Spacing between two images on the grid.

    Methods
    -------
    """

    def __init__(self, **kw):
        super().__init__(**kw)

    font = StringProperty("Roboto")
    label_height = 60 * scale_image
    spacing = global_spacing["horizontal"]
    add_image_image = ADD_IMAGE_SOURCE
    gallery_name = StringProperty("")
    number_cols = 3
    gallery_name_hint_text = StringProperty("")

    def init_screen(self, gallery: Gallery):
        """
        Initialize the screen when it is opened to create all the components to display.
        """
        # Reload the language
        self.gallery_name_hint_text = my_language.dict_language[
            "gallery"]["gallery_name_hint_text"]
        self.font = my_language.font

        # Set the function to the return button
        self.ids.top_menu_layout.ids.return_button.on_release = partial(
            self.go_to_next_screen, "menu")
        self.gallery = gallery
        self.gallery_name = gallery.name
        self.ids.my_sv_layout.reset_screen()
        self.build_scroll_view()

    def build_side_layout(self, label_text, side):
        """
        Build the display associated to one side during the screen initialisation.
        """

        # Label with the two badges
        best_category, _ = self.gallery.get_best_category(
            side=side)
        relative_layout = RelativeLayout(
            height=self.label_height,
            size_hint=(1, None)
        )
        label = Label(
            text=label_text,
            color=color_label,
            height=relative_layout.height,
            font_name=self.font
        )
        relative_layout.add_widget(label)
        badge_ratio = 1.3
        # Two badges to indicate the best category
        if best_category is not None:
            left_badge = Image(
                source=PATH_APP_IMAGES + best_category + ".png",
                size_hint=(None, None),
                height=relative_layout.height / badge_ratio,
                width=relative_layout.height / badge_ratio,
                pos_hint={"x": 0.2, "y": 0.1},
                allow_stretch=True
            )
            relative_layout.add_widget(left_badge)
            right_badge = Image(
                source=PATH_APP_IMAGES + best_category + ".png",
                size_hint=(None, None),
                height=relative_layout.height / badge_ratio,
                width=relative_layout.height / badge_ratio,
                pos_hint={"right": 0.8, "y": 0.1},
                allow_stretch=True
            )
            relative_layout.add_widget(right_badge)
        self.ids.my_sv_layout.add_widget(relative_layout)

        # Layout with all images
        list_images = self.gallery.get_list_side_images(side=side)
        number_images = len(list_images)
        height = (window_size[0] - self.label_height) / self.number_cols
        padding_side = 0.05 * window_size[0]
        stack_layout = StackLayout(
            spacing=self.spacing,
            padding=[padding_side, 0, padding_side, 0],
            size_hint_y=None,
            height=height * ceil(number_images / self.number_cols)
        )

        # Sort list per category
        order = {key: i for i, key in enumerate(
            list(DICT_CATEGORY_IMAGES.keys()))}
        list_images.sort(key=lambda image: order[image.category])

        # Display all badged images
        for tramway_image in list_images:
            badged_image = BadgedImage(
                size_hint=(None, None),
                width=(window_size[0] - padding_side * 2 - self.spacing *
                       (self.number_cols - 1)) / self.number_cols,
                height=height,
                tramway_image=tramway_image
            )
            badged_image.assign_function(
                function=partial(self.go_to_next_screen,
                                 "image_edition",
                                 tramway_image)
            )
            stack_layout.add_widget(badged_image)
        self.ids.my_sv_layout.add_widget(stack_layout)

    def build_scroll_view(self):
        """
        Build the scrollview containing the images for the display.
        """
        self.build_side_layout(
            my_language.dict_language["image_edition"]["left_side"],
            "left")
        self.build_side_layout(
            my_language.dict_language["image_edition"]["right_side"],
            "right")

    def go_to_next_screen(self, next_screen="menu", tramway_image=None):
        """
        Open the next screen with the choosed parameters.
        """
        try:
            has_changed = my_collection.change_name_gallery(
                my_gallery=self.gallery,
                new_name=self.ids.name_gallery_input.text
            )
        except ValueError:
            has_changed = False
            create_standard_popup(
                title_popup=my_language.dict_messages["error_gallery_name"][0],
                message=my_language.dict_messages["error_gallery_name"][1]
            )
            return
        if has_changed:
            save_collection()
        if next_screen != "menu":
            self.manager.init_screen(
                next_screen,
                gallery=self.gallery,
                tramway_image=tramway_image
            )
        else:
            self.manager.init_screen(next_screen)
