###############
### Imports ###
###############


### Python import ###

import os
import shutil
import time
from typing import Literal
from functools import partial

### Kivy imports ###

from kivy.uix.screenmanager import Screen
from kivy.uix.image import Image
from kivy.uix.popup import Popup
from kivy.properties import StringProperty
from kivy.clock import Clock

### Module imports ###

from tools.tools import (
    DICT_CATEGORY_IMAGES,
    PATH_RESOURCES_FOLDER,
    PATH_TUTORIAL_IMAGES,
    DICT_LANGUAGE_IMAGES_TUTORIAL,
    DICT_LANGUAGE_CORRESPONDANCE,
    SETTINGS,
    PATH_TRAMWAY_IMAGES,
    PATH_DATA_APP_FOLDER,
    MOBILE_MODE,
    my_language,
    __version__,
    detect_single_multiple_galleries,
)
from tools.tools_kivy import (
    window_size,
    ImprovedPopup,
    TutorialPopup,
    create_standard_popup
)
from tools.tools_collection import update_collection
from screens.image_edition_window import my_collection
from screens.components import LoadDialog

if MOBILE_MODE:
    from androidstorage4kivy import SharedStorage, Chooser, ShareSheet  # type: ignore

#####################
### Settings menu ###
#####################


class SettingsWindow(Screen):
    """
    Class displaying the settings menu
    """

    def __init__(self, **kw):
        super().__init__(**kw)
        self.choosed_status = "None"

    default_language = StringProperty(
        DICT_LANGUAGE_CORRESPONDANCE[SETTINGS["language"]])
    font = StringProperty("Roboto")
    list_languages = list(DICT_LANGUAGE_CORRESPONDANCE.values())
    window_size = window_size
    statistics_nb_galleries = StringProperty("0")
    label_nb_left = StringProperty("")
    label_nb_right = StringProperty("")
    statistics_nb_left_gold = StringProperty("0")
    statistics_nb_right_gold = StringProperty("0")
    statistics_nb_left_silver = StringProperty("0")
    statistics_nb_right_silver = StringProperty("0")
    statistics_nb_left_bronze = StringProperty("0")
    statistics_nb_right_bronze = StringProperty("0")
    dict_category_images = DICT_CATEGORY_IMAGES

    TEXT_SETTINGS = my_language.dict_language["settings"]
    language_label = StringProperty("")
    statistics_label = StringProperty("")
    tutorial_label = StringProperty("")
    version_label = StringProperty("")

    def init_screen(self):
        # Reload the language
        self.TEXT_SETTINGS = my_language.dict_language["settings"]
        self.language_label = self.TEXT_SETTINGS["language"]
        self.statistics_label = self.TEXT_SETTINGS["statistics"]["title"]
        self.tutorial_label = self.TEXT_SETTINGS["tutorial"]["title"]
        self.label_nb_left = my_language.dict_language["image_edition"]["left_side"]
        self.label_nb_right = my_language.dict_language["image_edition"]["right_side"]
        self.font = my_language.font

        # Set the function to the return button
        self.ids.top_menu_layout.ids.return_button.on_release = \
            self.ids.top_menu_layout.back_to_general

        # Get statistics
        statistics = my_collection.get_statistics()
        self.statistics_nb_galleries = str(statistics["total"]) + \
            detect_single_multiple_galleries(statistics["total"])
        self.statistics_nb_left_gold = str(statistics["gold"][0]) + \
            detect_single_multiple_galleries(statistics["gold"][0])
        self.statistics_nb_right_gold = str(statistics["gold"][1]) + \
            detect_single_multiple_galleries(statistics["gold"][1])
        self.statistics_nb_left_silver = str(statistics["silver"][0]) + \
            detect_single_multiple_galleries(statistics["silver"][0])
        self.statistics_nb_right_silver = str(statistics["silver"][1]) + \
            detect_single_multiple_galleries(statistics["silver"][1])
        self.statistics_nb_left_bronze = str(statistics["bronze"][0]) + \
            detect_single_multiple_galleries(statistics["bronze"][0])
        self.statistics_nb_right_bronze = str(statistics["bronze"][1]) + \
            detect_single_multiple_galleries(statistics["bronze"][1])

    def change_language(self):
        language = self.ids.language_spinner.text
        my_language.convert_language_code(language)
        my_language.change_language()
        self.init_screen()

    def wait_for_image(self, *args):
        if self.choosed_status != "Done":
            Clock.schedule_once(self.wait_for_image, 0.05)
        else:
            self.import_collection(None, self.private_files)
            self.choosed_status = "None"

    def chooser_callback(self, shared_file_list):
        self.private_files = []
        ss = SharedStorage()
        for shared_file in shared_file_list:
            self.private_files.append(ss.copy_from_shared(shared_file))
        self.choosed_status = "Done"

    def open_confirmation_popup(self):
        # Create the popup
        popup = ImprovedPopup(
            title=my_language.dict_messages["import_confirmation"][0],
            add_content=[],
            font=self.font)

        # Add the label, the progress bar and the button to close the window
        popup.add_label(
            text=my_language.dict_messages["import_confirmation"][1],
            pos_hint={"x": 0.1, "y": 0.6},
            size_hint=(0.8, 0.15),
            font_name=self.font
        )
        popup.add_button(
            text=my_language.dict_buttons["yes"],
            pos_hint={"x": 0.1, "y": 0.25},
            size_hint=(0.35, 0.15),
            on_release=partial(self.show_file_explorer, "IMPORT", popup),
            font_name=self.font
        )
        popup.add_button(
            text=my_language.dict_buttons["no"],
            pos_hint={"x": 0.55, "y": 0.25},
            size_hint=(0.35, 0.15),
            on_release=popup.dismiss,
            font_name=self.font
        )

    def show_file_explorer(self, mode: Literal["IMPORT", "EXPORT"], popup=None):
        if popup is not None:
            popup.dismiss()
        if MOBILE_MODE:
            self.chooser = Chooser(self.chooser_callback)
            if mode == "IMPORT":
                self.chooser.choose_content("application/zip")
                self.wait_for_image()
            else:
                self.export_collection(None, None)
        else:
            my_callback = self.import_collection
            title_popup = self.TEXT_SETTINGS["import_collection"]
            if mode == "EXPORT":
                my_callback = self.export_collection
                title_popup = self.TEXT_SETTINGS["export_collection"]
            content = LoadDialog(load=my_callback,
                                 cancel=self.dismiss_popup, filters_list=["*.zip"])
            self.file_chooser = Popup(
                title=title_popup,
                content=content,
                size_hint=(0.9, 0.9),
                title_font=self.font)
            self.file_chooser.open()

    def dismiss_popup(self):
        self.file_chooser.dismiss()

    def import_collection(self, path, filename):
        # Close the file explorer
        if not MOBILE_MODE:
            self.dismiss_popup()

        # Delete the previous collection
        shutil.rmtree(PATH_TRAMWAY_IMAGES)

        # Unpack the archive
        shutil.unpack_archive(filename[0], PATH_TRAMWAY_IMAGES)
        update_collection()
        self.init_screen()

        # Display a completion popup
        create_standard_popup(
            title_popup=my_language.dict_messages["import_completed"][0],
            message=my_language.dict_messages["import_completed"][1],
            button_message=my_language.dict_buttons["close"]
        )

    def export_collection(self, path, filename):

        # Close the file explorer
        if not MOBILE_MODE:
            self.dismiss_popup()

        # Zip the collection
        if MOBILE_MODE:
            # Create the zip file
            shutil.make_archive(PATH_DATA_APP_FOLDER +
                                "collection", "zip", PATH_TRAMWAY_IMAGES)

            # Copy it into the shared storage
            shared_storage = SharedStorage()
            file_to_share = shared_storage.copy_to_shared(PATH_DATA_APP_FOLDER +
                                                          "collection.zip", filepath="/collection.zip")

            # Share it
            shared_sheet = ShareSheet()
            shared_sheet.share_file(file_to_share)
        else:
            shutil.make_archive(path +
                                "/collection", "zip", PATH_TRAMWAY_IMAGES)

        # Display a completion popup
        create_standard_popup(
            title_popup=my_language.dict_messages["export_completed"][0],
            message=my_language.dict_messages["export_completed"][1],
            button_message=my_language.dict_buttons["close"]
        )

    def display_credits(self):
        """
        Display the credits in a popup.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """

        # Create the layout of the popup composed of the label
        popup_messages = self.TEXT_SETTINGS["credits_popup"]
        popup_content = [
            ("label", {
                "text": popup_messages["label_popup"].replace("###", __version__),
                "pos_hint": {"x": 0.1, "y": 0.7},
                "size_hint": (0.8, 0.15),
                "font_name": self.font
            }
            )
        ]

        # Create the popup
        popup = ImprovedPopup(
            title=popup_messages["title_popup"],
            add_content=popup_content,
            font=self.font)

        # Add the logo
        popup.add_other_widget(
            Image,
            source=PATH_RESOURCES_FOLDER + "logo_collector_1024.png",
            pos_hint={"x": 0.2, "y": 0.3},
            size_hint=(0.6, 0.35),
            allow_stretch=True
        )

        # Add the close button
        popup.add_button(
            text=my_language.dict_buttons["close"],
            pos_hint={"x": 0.2, "y": 0.1},
            size_hint=(0.6, 0.15),
            on_release=popup.dismiss,
            font_name=self.font
        )

    def launch_tutorial(self):
        text_tutorial = self.TEXT_SETTINGS["tutorial"]
        language_images_tutorial = DICT_LANGUAGE_IMAGES_TUTORIAL[my_language.code_language]
        dict_images = {
            "welcome": PATH_RESOURCES_FOLDER + "logo.png",
            "choice_side": PATH_TUTORIAL_IMAGES + "tutorial_" +
            language_images_tutorial + "_cover_image.png",
            "choice_category": PATH_TUTORIAL_IMAGES + "tutorial_" +
            language_images_tutorial + "_left_right.png",
            "default": PATH_TUTORIAL_IMAGES + "tutorial_quality.png"
        }

        # Extract content for the json file of the language
        list_popups = []
        for key in text_tutorial["tutorial_content"]:
            dict_popup = text_tutorial["tutorial_content"][key]
            if key in dict_images:
                dict_popup["image"] = dict_images[key]
            list_popups.append(dict_popup)

        # Change name for the first and last buttons
        list_popups[0]["left_button"] = text_tutorial["cancel_button"]

        list_popups[-1]["right_button"] = text_tutorial["finish_button"]

        # Build tutorial
        TutorialPopup(
            list_popups=list_popups, font=self.font
        )
