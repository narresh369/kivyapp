# main.py
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
import os

# Import actual screen implementations
from screens.register_screen import RegisterScreen
from screens.tracker_screen import TrackerScreen


class MainScreen(Screen):
    def go_to_register(self, instance):
        self.manager.current = "register"

    def go_to_tracker(self, instance):
        self.manager.current = "tracker"

    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')
        layout.add_widget(Button(text="Go to Register",
                                 on_press=self.go_to_register))
        layout.add_widget(Button(text="Go to Tracker",
                                 on_press=self.go_to_tracker))
        self.add_widget(layout)


class MyApp(App):


    def build(self):
        sm = ScreenManager()
        sm.add_widget(MainScreen(name='main'))
        sm.add_widget(RegisterScreen(name='register'))

        # Wrap TrackerScreen (a layout) inside a Screen
        tracker_screen = Screen(name='tracker')
        tracker_screen.add_widget(TrackerScreen())
        sm.add_widget(tracker_screen)

        return sm



if __name__ == '__main__':
    MyApp().run()
