"""
Main script to launch Tramway Collector
"""


###############
### Imports ###
###############


### Python import ###

import os

### Kivy imports ###

from kivy.config import Config
Config.set('kivy', 'exit_on_escape', '0')
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import ScreenManager, NoTransition, Screen
from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.app import App

### Module imports ###

from tools import (
    clean_unused_images,
    highlight_text_color,
    pink_color,
    blue_color,
    color_label,
    Window,
    background_color,
    window_size,
    PATH_RESOURCES_FOLDER,
    PATH_KIVY_FOLDER
)
from screens import (
    MenuWindow,
    CollectionWindow,
    GalleryWindow,
    ImageEditionWindow,
    SettingsWindow
)


######################
### Global classes ###
######################


class TopMenuLayout(FloatLayout):
    """
    Class displaying the top of each menu
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    path_resources = PATH_RESOURCES_FOLDER

    def back_to_general(self):
        """
        Function to reopen the main menu.

        Used when clicking on the tramway icon at the top.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        self.parent.manager.init_screen("menu")


class MyScrollViewLayout(GridLayout):
    """
    Class corresponding to the layout inside the scroll view
    """

    def __init__(self, **kwargs):
        super(MyScrollViewLayout, self).__init__(**kwargs)
        self.size_hint_y = None
        self.bind(minimum_height=self.setter('height'))

    def reset_screen(self):
        """
        Removes all widgets from the scrollview.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        list_widgets = self.children[:]
        for element in list_widgets:
            self.remove_widget(element)


###############
### General ###
###############


class WindowManager(ScreenManager):
    """
    Screen manager, which allows the navigations between the different menus.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.highlight_text_color = highlight_text_color
        self.button_disabled_color = (
            382 / 255, 382 / 255, 382 / 255, 1)
        self.pink_color = pink_color
        self.blue_color = blue_color
        self.color_label = color_label
        self.transition = NoTransition()
        self.add_widget(Screen(name="opening"))
        self.current = "opening"
        self.list_former_screens = []

    def init_screen(self, screen_name, gallery=None, tramway_image=None):
        """
        Init the selected screen with the given informations and change the screen.

        Parameters
        ----------
        screen_name : str
            Name of the screen.

        gallery : Gallery | None, optional (default is None)
            Gallery to use to load the screen if one is needed.

        tramway_image : TramwayImage | None, optional (default is None)
            TramwayImage instance to use to load the screen if one is needed.

        Returns
        -------
        None
        """
        self.list_former_screens.append(self.current)
        self.current = screen_name
        if screen_name in ["collection", "settings", "menu"]:
            self.get_screen(screen_name).init_screen()
        if screen_name == "image_edition":
            self.get_screen("image_edition").init_screen(
                gallery=gallery,
                tramway_image=tramway_image
            )
        if screen_name == "gallery":
            self.get_screen("gallery").init_screen(
                gallery=gallery
            )


class MainApp(App, Widget):
    """
    Main class of the application.
    """

    def build(self):
        """
        Build the application.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        Window.clearcolor = background_color
        Window.size = window_size
        self.icon = PATH_RESOURCES_FOLDER + "logo_collector_1024.png"
        Window.bind(on_keyboard=self.key_input)

    def on_start(self):
        self.root_window.children[0].init_screen("menu")
        return super().on_start()

    def key_input(self, window, key, scancode, codepoint, modifier):
        """
        Take into account the back arrow in Android, corresponding to the key 27 (escape).

        Parameters
        ----------
        window
        key
        scancode
        codepoint
        modifier

        Returns
        -------
        None
        """
        if key == 27:
            screen_manager: WindowManager = self._app_window.children[0]
            if len(screen_manager.list_former_screens) > 1:
                self._app_window.children[0].current = screen_manager.list_former_screens.pop(
                )
                return True
        return False


# Run the application
if __name__ == "__main__":
    for file_name in os.listdir(PATH_KIVY_FOLDER):
        if file_name.endswith(".kv"):
            Builder.load_file(PATH_KIVY_FOLDER + file_name, encoding="utf-8")
    MainApp().run()

clean_unused_images()
