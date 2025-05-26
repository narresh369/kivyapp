# tracker_screen.py

from kivy.uix.boxlayout import BoxLayout
from kivy_garden.mapview import MapView


class TrackerScreen(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'

        # Create a MapView centered at a default location
        # Hyderabad as default
        map_view = MapView(zoom=10, lat=17.385044, lon=78.486671)
        self.add_widget(map_view)
