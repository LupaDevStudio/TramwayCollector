"""
Module to define the Kivy content of the image edition screen.

Classes
-------
ImageEditionWindow : content of the image edition screen.
"""


###############
### Imports ###
###############

### Python imports ###

from functools import partial
import os
import time

### Kivy imports ###

from kivy.uix.screenmanager import Screen
from kivy.uix.popup import Popup
from kivy.properties import StringProperty, BooleanProperty
from kivy.clock import Clock

### Module imports ###

from tools.tools import (
    EMPTY_IMAGE_SOURCE,
    DICT_CATEGORY_IMAGES,
    PATH_APP_IMAGES,
    DICT_BADGES_IMAGES,
    PATH_TRAMWAY_IMAGES,
    PATH_TEMP_IMAGE,
    MOBILE_MODE,
    my_language,
    update_settings,
)
from tools.tools_collection import (
    Gallery,
    TramwayImage,
    save_collection
)
from tools.tools_kivy import (
    ImprovedPopup,
    create_standard_popup
)
from tools.tools_image import (
    IMAGE_EXT,
    copy_as_square,
    transfer_temp_image,
    create_new_image_name
)
from screens.gallery_window import my_collection
from screens.components import LoadDialog


if MOBILE_MODE:
    from androidstorage4kivy import SharedStorage, Chooser, ShareSheet  # type: ignore


##########################
### Image edition menu ###
##########################


class ImageEditionWindow(Screen):
    """
    Screen to display the collection.
    """

    def __init__(self, **kw):
        super().__init__(**kw)

    gallery_name = StringProperty("")
    path_preview_image = StringProperty(EMPTY_IMAGE_SOURCE)
    is_new_image = BooleanProperty(True)
    is_new_gallery = BooleanProperty(True)
    category = StringProperty("")
    dict_category_images = {
        "gold": [DICT_CATEGORY_IMAGES["gold"], PATH_APP_IMAGES + "gold_off.png"],
        "silver": [DICT_CATEGORY_IMAGES["silver"], PATH_APP_IMAGES + "silver_off.png"],
        "bronze": [DICT_CATEGORY_IMAGES["bronze"], PATH_APP_IMAGES + "bronze_off.png"]
    }
    side_tramway = StringProperty("")
    bool_default = BooleanProperty(False)
    plus_plus_images = DICT_BADGES_IMAGES["plus_plus"]
    bool_plus_plus = BooleanProperty(False)

    # Language variables
    font = StringProperty("Roboto")
    gallery_name_hint_text = StringProperty("")
    browse_button_text = StringProperty("")
    delete_button_text = StringProperty("")
    left_side_label = StringProperty("")
    right_side_label = StringProperty("")
    on_label = StringProperty("")
    off_label = StringProperty("")
    default_label = StringProperty("")
    add_button_text = StringProperty("")
    modify_button_text = StringProperty("")

    def init_screen(self, gallery: Gallery, tramway_image=None):
        """
        Initialize the screen when it is opened to create all the components to display.
        """
        # Reload the language
        self.gallery_name_hint_text = my_language.dict_language[
            "image_edition"]["gallery_name_hint_text"]
        self.browse_button_text = my_language.dict_language[
            "image_edition"]["browse_button"]
        self.delete_button_text = my_language.dict_language[
            "image_edition"]["delete_button"]
        self.left_side_label = my_language.dict_language[
            "image_edition"]["left_side"]
        self.right_side_label = my_language.dict_language[
            "image_edition"]["right_side"]
        self.on_label = my_language.dict_language[
            "image_edition"]["on"]
        self.off_label = my_language.dict_language[
            "image_edition"]["off"]
        self.default_label = my_language.dict_language[
            "image_edition"]["default_label"]
        self.add_button_text = my_language.dict_language[
            "image_edition"]["add_button"]
        self.modify_button_text = my_language.dict_language[
            "image_edition"]["modify_button"]
        self.font = my_language.font

        # Set the function to the return button
        self.ids.top_menu_layout.ids.return_button.on_release = self.back_to_gallery

        self.gallery = gallery
        self.gallery_name = gallery.name
        self.ids.name_gallery_input.text = self.gallery_name

        # Check whether it's a new gallery or not
        self.is_new_gallery = True
        if self.gallery_name != "":
            self.is_new_gallery = False

        # Configure the screen whether it's a new image or not
        if tramway_image != None:
            self.is_new_image = False
            self.ids.add_button.disabled = False

            # Init toggle buttons for the sides
            if tramway_image.side == "left":
                self.ids.left_side_toggle.state = "down"
                self.ids.right_side_toggle.state = "normal"
            else:
                self.ids.left_side_toggle.state = "normal"
                self.ids.right_side_toggle.state = "down"
        else:
            self.is_new_image = True
            self.ids.add_button.disabled = True
            tramway_image = TramwayImage(default=False)

        self.tramway_image = tramway_image
        self.path_preview_image = tramway_image.source
        self.category = str(tramway_image.category)
        self.side_tramway = str(tramway_image.side)
        self.bool_default = tramway_image.default
        self.bool_plus_plus = tramway_image.plus_plus

    def exit_manager(self, *args):
        """
        Close the file manager.
        """
        self.file_manager.close()

    def select_path(self, path):
        """
        Select the path to load the image when choosing one in the file manager.
        """
        self.exit_manager()
        self.load_image(path)

    def share_image(self):
        # Copy it into the shared storage
        shared_storage = SharedStorage()
        file_to_share = shared_storage.copy_to_shared(
            self.tramway_image.source, filepath="/image_to_share.jpeg")

        # Share it
        shared_sheet = ShareSheet()
        shared_sheet.share_file(file_to_share)

    def dismiss_popup(self):
        self.file_chooser.dismiss()

    def wait_for_image(self, *args):
        if self.choosed_status != "Done":
            Clock.schedule_once(self.wait_for_image, 0.05)
        else:
            self.load_image(None, self.private_files)
            self.choosed_status = "None"

    def show_load(self):
        if MOBILE_MODE:
            self.choosed_status = "None"
            self.chooser = Chooser(self.chooser_callback)
            self.chooser.choose_content("image/*")
            self.wait_for_image()

        else:
            content = LoadDialog(load=self.load_image,
                                 cancel=self.dismiss_popup,
                                 filters_list=['*.png', '*.jpeg', '*.jpg', '*.PNG', '*.JPEG', '*.JPG'])
            self.file_chooser = Popup(
                title=my_language.dict_language[
                    "image_edition"]["load_image"],
                content=content,
                size_hint=(0.9, 0.9),
                title_font=self.font)
            self.file_chooser.open()

    def chooser_callback(self, shared_file_list):
        self.private_files = []
        ss = SharedStorage()
        for shared_file in shared_file_list:
            self.private_files.append(ss.copy_from_shared(shared_file))
        # while not os.path.exists(self.private_files[0]):
        #     time.sleep(0.1)
        # self.load_image(None, self.private_files)
        self.choosed_status = "Done"

    def load_image(self, path, filename):
        if not MOBILE_MODE:
            self.dismiss_popup()

        # Load the image for preview in the temp folder
        copy_as_square(filename[0], temp=True)
        self.path_preview_image = PATH_TEMP_IMAGE
        self.ids.preview_image.reload()

        # Disable the add button
        self.ids.add_button.disabled = False

        # Update default path in the settings
        update_settings("default_path_images", os.path.dirname(filename[0]))

    def delete_image(self, popup: ImprovedPopup):
        # Delete the image in the gallery
        self.gallery.delete_image(tramway_image=self.tramway_image)

        # Delete the gallery in the collection if it is empty
        is_empty = self.gallery.check_is_empty()
        if is_empty:
            my_collection.delete_gallery(self.gallery)
        else:
            # Set a new default image
            if self.tramway_image.default:
                self.gallery.set_new_random_default(
                    side=self.tramway_image.side)

        # Save the collection
        save_collection()

        # Return to gallery menu or general menu if the gallery has been deleted
        popup.dismiss()
        self.back_to_gallery()

    def back_to_gallery(self):
        is_empty = self.gallery.check_is_empty()
        if is_empty:
            self.manager.init_screen("menu")
        else:
            self.manager.init_screen("gallery", gallery=self.gallery)

    def create_popup_delete_confirmation(self):
        # Create the popup
        popup = ImprovedPopup(
            title=my_language.dict_messages["delete_confirmation"][0],
            add_content=[],
            font=self.font)

        # Add the label, the progress bar and the button to close the window
        popup.add_label(
            text=my_language.dict_messages["delete_confirmation"][1],
            pos_hint={"x": 0.1, "y": 0.6},
            size_hint=(0.8, 0.15),
            font_name=self.font
        )
        popup.add_button(
            text=my_language.dict_buttons["yes"],
            pos_hint={"x": 0.1, "y": 0.25},
            size_hint=(0.35, 0.15),
            on_release=partial(self.delete_image, popup),
            font_name=self.font
        )
        popup.add_button(
            text=my_language.dict_buttons["no"],
            pos_hint={"x": 0.55, "y": 0.25},
            size_hint=(0.35, 0.15),
            on_release=popup.dismiss,
            font_name=self.font
        )

    def add_image(self):

        # Check that the name of the gallery is not empty
        if self.ids.name_gallery_input.text == "":
            create_standard_popup(
                title_popup=my_language.dict_messages["error_gallery_name"][0],
                message=my_language.dict_messages["error_gallery_name"][1]
            )
            return

        # Check that a side has been selected
        if self.side_tramway == "None":
            create_standard_popup(
                title_popup=my_language.dict_messages["error_no_side"][0],
                message=my_language.dict_messages["error_no_side"][1]
            )
            return

        # Check that a category has been selected
        if self.category == "None":
            create_standard_popup(
                title_popup=my_language.dict_messages["error_no_category"][0],
                message=my_language.dict_messages["error_no_category"][1]
            )
            return

        # Save the parameters of the image
        if self.is_new_image:
            new_image_name = create_new_image_name()
            transfer_temp_image(new_image_name)
            path = PATH_TRAMWAY_IMAGES + new_image_name + IMAGE_EXT
            self.tramway_image.source = path

        self.tramway_image.side = self.side_tramway
        self.tramway_image.category = self.category
        self.tramway_image.plus_plus = self.bool_plus_plus
        if self.bool_default:
            self.gallery.update_default_image(
                tramway_image=self.tramway_image
            )

        # Add the new gallery in the collection
        if self.is_new_gallery:
            self.gallery.name = self.ids.name_gallery_input.text
            try:
                my_collection.add_gallery(gallery=self.gallery)
            except ValueError:
                create_standard_popup(
                    title_popup=my_language.dict_messages["error_gallery_name"][0],
                    message=my_language.dict_messages["error_gallery_name"][1]
                )
                return

        # Add the new image in the gallery
        if self.is_new_image:
            self.gallery.add_image(tramway_image=self.tramway_image)
        self.gallery.assign_default_image()

        # Save collection and return to gallery menu
        save_collection()
        self.back_to_gallery()
