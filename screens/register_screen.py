import re
import time
from threading import Thread
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.uix.screenmanager import Screen
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.storage.jsonstore import JsonStore

import json
import requests
FIRESTORE_PROJECT_ID = "savealife-7a219"
API_KEY = "AIzaSyAxv4vdzh6lrE9GrjFcmACLQ9-EBb1I6Ck"  # Your Firebase Web API Key
FIRESTORE_URL = f"https://firestore.googleapis.com/v1/projects/{FIRESTORE_PROJECT_ID}/databases/(default)/documents/users"

store = JsonStore("user_data.json")
class RegisterScreen(Screen):

    #def __init__(self, db, **kwargs):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        #self.db = db
        layout = BoxLayout(orientation="vertical", padding=10, spacing=10)

        with layout.canvas.before:
            from kivy.graphics import Color, Rectangle
            Color(0.0, 0.0, 0.502, 1)
            self.bg_rect = Rectangle(pos=layout.pos, size=layout.size)
        layout.bind(pos=self._update_rect, size=self._update_rect)

        # Input fields
        layout.add_widget(Label(text="Personal Details"))
        self.name_input = TextInput(hint_text="Full Name")
        self.phone = TextInput(hint_text="Phone Number")
        self.address = TextInput(hint_text="Address")
        layout.add_widget(self.name_input)
        layout.add_widget(self.phone)
        layout.add_widget(self.address)

        layout.add_widget(Label(text="Family Contact"))
        self.family_name = TextInput(hint_text="Family Member Name")
        self.family_phone = TextInput(hint_text="Family Member Phone")
        layout.add_widget(self.family_name)
        layout.add_widget(self.family_phone)

        layout.add_widget(Label(text="Health Information"))
        self.blood_type = TextInput(hint_text="Blood Type (e.g., A+)")
        self.allergies = TextInput(hint_text="Allergies")
        layout.add_widget(self.blood_type)
        layout.add_widget(self.allergies)

        layout.add_widget(Label(text="Insurance Details"))
        self.insurance_provider = TextInput(hint_text="Insurance Provider")
        self.policy_number = TextInput(hint_text="Policy Number")
        layout.add_widget(self.insurance_provider)
        layout.add_widget(self.policy_number)

        submit_btn = Button(text="Register", background_color=(0, 1, 0, 1))
        submit_btn.bind(on_press=self._on_register_press)
        layout.add_widget(submit_btn)

        back_btn = Button(text="Back", size_hint=(1, None), height=40)
        back_btn.bind(on_press=lambda x: (
            self.animate_button_press(x), self.go_back()))
        layout.add_widget(back_btn)

        scroll = ScrollView()
        scroll.add_widget(layout)
        self.add_widget(scroll)

    def _on_register_press(self, button):
        self.animate_button_press(button)
        Thread(target=self.save_data, daemon=True).start()

    def _update_rect(self, instance, value):
        self.bg_rect.pos = instance.pos
        self.bg_rect.size = instance.size

    def go_back(self):
        App.get_running_app().root.current = "home"

    def show_popup(self, title, message):
        popup_layout = BoxLayout(
            orientation='vertical', padding=10, spacing=10)
        popup_layout.add_widget(Label(text=message))
        close_btn = Button(text='OK', size_hint=(1, 0.3))
        popup_layout.add_widget(close_btn)

        popup = Popup(title=title, content=popup_layout,
                      size_hint=(0.8, 0.4), auto_dismiss=False)
        close_btn.bind(on_press=popup.dismiss)
        popup.open()

    def show_loading(self, message="Please wait..."):
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        label = Label(text=message, font_size='16sp')
        layout.add_widget(label)
        self.loading_popup = Popup(title="Loading",
                                   content=layout,
                                   size_hint=(None, None),
                                   size=(300, 150),
                                   auto_dismiss=False)
        self.loading_popup.open()

    def hide_loading(self):
        if hasattr(self, 'loading_popup') and self.loading_popup:
            self.loading_popup.dismiss()

    @staticmethod
    def animate_button_press(button):
        original_color = button.background_color
        pressed_color = [c * 0.7 for c in original_color[:3]] + [1]
        anim_down = Animation(background_color=pressed_color, duration=0.05)
        anim_up = Animation(background_color=original_color, duration=0.1)
        anim_down.bind(on_complete=lambda *args: anim_up.start(button))
        anim_down.start(button)

    def save_data(self):
        Clock.schedule_once(lambda dt: self.show_loading("Registering user..."), 0)

        phone_number = self.phone.text.strip()
        family_phone = self.family_phone.text.strip()
        name = self.name_input.text.strip()
        address = self.address.text.strip()
        family_name = self.family_name.text.strip()
        blood_type = self.blood_type.text.strip()
        allergies = self.allergies.text.strip()
        insurance_provider = self.insurance_provider.text.strip()
        policy_number = self.policy_number.text.strip()

        if not phone_number.startswith("+91"):
            phone_number = "+91" + phone_number.lstrip("0")
        if family_phone and not family_phone.startswith("+91"):
            family_phone = "+91" + family_phone.lstrip("0")

        required_fields = {
            "Name": name, "Phone number": phone_number, "Address": address,
            "Family Name": family_name, "Family Phone": family_phone,
            "Blood Type": blood_type, "Allergies": allergies,
            "Insurance Provider": insurance_provider, "Policy Number": policy_number
        }

        for field, value in required_fields.items():
            if not value:
                Clock.schedule_once(lambda dt: (
                    self.hide_loading(),
                    self.show_popup("Missing Field", f"{field} is required.")
                ), 0)
                return

        phone_pattern = re.compile(r"^\+91[6-9]\d{9}$")
        if not phone_pattern.match(phone_number):
            Clock.schedule_once(lambda dt: (
                self.hide_loading(),
                self.show_popup(
                    "Invalid Number", "Enter a valid 10-digit phone number starting with 6-9.")
            ), 0)
            return

        if not phone_pattern.match(family_phone):
            Clock.schedule_once(lambda dt: (
                self.hide_loading(),
                self.show_popup("Invalid Family Number",
                                "Enter a valid 10-digit family phone number starting with 6-9.")
            ), 0)
            return

        # Prepare data in Firestore format
        user_data = {
            "fields": {
                "name": {"stringValue": name},
                "phone": {"stringValue": phone_number},
                "address": {"stringValue": address},
                "family_name": {"stringValue": family_name},
                "family_phone": {"stringValue": family_phone},
                "blood_type": {"stringValue": blood_type},
                "allergies": {"stringValue": allergies},
                "insurance_provider": {"stringValue": insurance_provider},
                "policy_number": {"stringValue": policy_number}
            }
        }

        try:
            # Check if document already exists (via structured query)
            check_url = f"https://firestore.googleapis.com/v1/projects/{FIRESTORE_PROJECT_ID}/databases/(default)/documents:runQuery?key={API_KEY}"
            query = {
                "structuredQuery": {
                    "from": [{"collectionId": "users"}],
                    "where": {
                        "fieldFilter": {
                            "field": {"fieldPath": "phone"},
                            "op": "EQUAL",
                            "value": {"stringValue": phone_number}
                        }
                    },
                    "limit": 1
                }
            }
            check_response = requests.post(check_url, json=query)
            if any("document" in doc for doc in check_response.json()):
                Clock.schedule_once(lambda dt: (
                    self.hide_loading(),
                    self.show_popup(
                        "Already Registered", "User with this phone number is already registered.")
                ), 0)
                return

            # Save data to Firestore
            post_url = f"{FIRESTORE_URL}?documentId={phone_number}&key={API_KEY}"
            response = requests.post(post_url, headers={
                                    "Content-Type": "application/json"}, data=json.dumps(user_data))

            if response.status_code == 200:
                store.put("user", phone=phone_number)
                Clock.schedule_once(lambda dt: (
                    self.hide_loading(),
                    self.show_popup("Success", "Registration successful!"),
                    setattr(App.get_running_app().root, "current", "home")
                ), 0)
            else:
                raise Exception(response.text)

        except Exception as e:
            Clock.schedule_once(lambda dt, err=str(e): (
                self.hide_loading(),
                self.show_popup("Error", f"Something went wrong:\n{err}")
            ), 0)
