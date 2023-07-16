"""
Module to define the Kivy content of the collection screen.

Classes
-------
CollectionWindow : content of the collection screen.
"""

###############
### Imports ###
###############


### Python imports ###

from functools import partial

### Kivy imports ###

from kivy.uix.gridlayout import GridLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.properties import StringProperty

### Module imports ###

from tools.tools import (
    ADD_IMAGE_SOURCE,
    EMPTY_IMAGE_SOURCE,
    FRAME_IMAGE_SOURCE,
    my_language
)
from tools.tools_kivy import (
    global_spacing,
    window_size,
    scale_image
)
from tools.tools_collection import (
    Gallery,
    TramwayImage
)
from screens.components import BadgedImage
from screens.menu_window import my_collection


#######################
### Collection menu ###
#######################


class CollectionWindow(Screen):
    """
    Screen to display the collection.

    Attributes
    ----------
    font : str
        Name of the font used to display the text.

    label_height : float
        Height of a label for the display.

    spacing : float
        Spacing between two images on the grid.

    padding : float
        Padding used for the grid display.

    Methods
    -------
    init_screen : initialize the screen for the display.

    build_image : create a single image on the screen.

    build_scrollview : build the scrollview with all images.

    add_image : open the image edition screen.
    """

    def __init__(self, **kw):
        super().__init__(**kw)

    font = StringProperty("Roboto")
    label_height = 40 * scale_image
    spacing = global_spacing["horizontal"]
    padding = global_spacing["horizontal"] * 2

    def init_screen(self):
        """
        Initialize the screen when it is opened to create all the components to display.
        """
        self.ids.my_sv_layout.reset_screen()
        self.ids.top_menu_layout.ids.return_button.on_release = \
            self.ids.top_menu_layout.back_to_general
        self.font = my_language.font
        self.build_scroll_view()

    def build_image(self, gallery: Gallery, side, height):
        """
        Load a single image from a gallery to display it on the screen.
        """
        tramway_image: TramwayImage = gallery.get_default_image(side)
        if tramway_image.source != EMPTY_IMAGE_SOURCE:
            image = BadgedImage(
                size_hint_y=None,
                height=height,
                tramway_image=tramway_image
            )
            image.assign_function(
                function=partial(self.manager.init_screen,
                                 "image_edition", gallery, tramway_image)
            )
            return image
        image = Image(
            size_hint_y=None,
            height=height,
            allow_stretch=True,
            source=FRAME_IMAGE_SOURCE
        )
        return image

    def build_scroll_view(self):
        """
        Build the scrollview containing the images to display them on the screen
        """
        grid_layout_width = window_size[0]
        height = (grid_layout_width - self.label_height) / 3
        for gallery in my_collection.list_galleries:
            # Label for the name of the gallery
            name_label = Label(
                size_hint_y=None,
                height=self.label_height,
                color=self.manager.color_label,
                text=gallery.name,
                font_name=self.font
            )
            self.ids.my_sv_layout.add_widget(name_label)

            # Grid layout for the three images
            grid_layout = GridLayout(
                cols=3,
                size_hint_y=None,
                padding=[self.padding, 0, self.padding, 0],
                spacing=[self.spacing, 0],
                width=grid_layout_width
            )
            grid_layout.height = height

            # Left image
            left_image = self.build_image(
                gallery, "left", height)
            grid_layout.add_widget(left_image)

            # Right image
            right_image = self.build_image(
                gallery, "right", height)
            grid_layout.add_widget(right_image)

            # Add image
            add_image_layout = RelativeLayout(
                size_hint_y=None,
                height=height
            )
            add_image = Image(
                size_hint_y=None,
                height=height / 2,
                pos_hint={"center_x": 0.5, "center_y": 0.5},
                source=ADD_IMAGE_SOURCE,
                allow_stretch=True
            )
            add_image_layout.add_widget(add_image)
            add_button = Button(
                size_hint_y=None,
                height=height / 2,
                pos_hint={"center_x": 0.5, "center_y": 0.5},
                background_color=(0, 0, 0, 0)
            )
            add_button.on_release = partial(self.add_image, gallery)
            add_image_layout.add_widget(add_button)
            grid_layout.add_widget(add_image_layout)

            self.ids.my_sv_layout.add_widget(grid_layout)

        # Add gallery

        # Empty label for spacing
        add_gallery_label = Label(
            size_hint_y=None,
            height=self.label_height,
            color=self.manager.color_label,
            text=my_language.dict_language["collection"]["new_gallery"],
            font_name=self.font
        )
        self.ids.my_sv_layout.add_widget(add_gallery_label)

        # Add button
        add_galery_layout = RelativeLayout(
            size_hint_y=None,
            height=height
        )
        add_gallery_image = Image(
            size_hint_y=None,
            height=height / 1.5,
            pos_hint={"center_x": 0.5, "center_y": 0.5},
            source=ADD_IMAGE_SOURCE,
            allow_stretch=True
        )
        add_galery_layout.add_widget(add_gallery_image)
        add_gallery_button = Button(
            size_hint_y=None,
            height=height / 1.5,
            pos_hint={"center_x": 0.5, "center_y": 0.5},
            background_color=(0, 0, 0, 0)
        )
        add_gallery_button.on_release = partial(
            self.add_image, Gallery())
        add_galery_layout.add_widget(add_gallery_button)
        self.ids.my_sv_layout.add_widget(add_galery_layout)

    def add_image(self, gallery: Gallery):
        """
        Open the image edition screen with the selected gallery.

        Parameters
        ----------
        gallery : Gallery
            Gallery to open.
        """
        self.manager.init_screen("image_edition", gallery=gallery)
