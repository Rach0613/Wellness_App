from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from hoverable import HoverBehavior
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior
import json
import glob
from datetime import datetime
from pathlib import Path
import random
from abc import ABC, abstractmethod


Builder.load_file('design.kv')


class Base1(ABC):
    @abstractmethod
    def method_from_base(self):
        pass


class Base2(ABC):
    @abstractmethod
    def method_from_base2(self):
        pass


class LoginScreen(Screen):
    def sign_up(self):
        self.manager.current = "sign_up_screen"

    def forgot_password(self):
        self.manager.current = "forgot_password_screen"

    def login(self, uname, pword):
        with open("users.json") as file:
            users = json.load(file)
        if uname in users and users[uname]["password"] == pword:
            self.manager.current = "login_screen_success"
        else:
            self.ids.login_wrong.text = "Wrong Username or Password!"


class RootWidget(ScreenManager):
    pass


class ForgotPasswordScreen(Screen):
    def validate_user(self, uname):
        with open("users.json") as file:
            users = json.load(file)

        if uname in users:
            password = users[uname]['password']
            self.ids.forgot_password.text = f" Your password is: {password}"
        else:
            self.ids.forgot_password.text = "Username is NOT FOUND! Please try again."

    def go_back_to_login(self):
        self.manager.current = "login_screen"


class ForgotPasswordScreenSuccess(Screen):
    def go_back_to_login(self):
        self.manager.transition.direction = "left"
        self.manager.current = "login_screen"


class SignUpScreen(Screen):
    def add_user(self, uname, pword):
        try:
            with open("users.json") as file:
                users = json.load(file)
        except FileNotFoundError:
            print("The file is NOT FOUND in the directory!. Creating a new file.")
            users = {}

        users[uname] = {'username': uname, 'password': pword,
                        'created': datetime.now().strftime("%Y-%m-%d %H-%M-%S")}
        print(users)

        try:
            with open("users.json", "w") as file:
                json.dump(users, file)
        except (Exception,):
            pass

        self.manager.current = "sign_up_screen_success"


class SignUpScreenSuccess(Screen):
    def go_to_login(self):
        self.manager.transition.direction = "right"
        self.manager.current = "login_screen"


class LoginScreenSuccess(Screen):
    def log_out(self):
        self.manager.transition.direction = "right"
        self.manager.current = "login_screen"

    def get_quote(self, feel):
        feel = feel.lower()
        available_feelings = glob.glob("quotes/*.txt", recursive=True)

        available_feelings = [Path(filename).stem for filename in available_feelings]

        if feel in available_feelings:
            with open(f"quotes/{feel}.txt", encoding="utf8") as file:
                quotes = file.readlines()
            self.ids.quote.text = random.choice(quotes)
        else:
            self.ids.quote.text = "Please try another feeling!"


class ImageButton(ButtonBehavior, HoverBehavior, Image):
    pass


class MainApp(App):
    def build(self):
        return RootWidget()


if __name__ == "__main__":
    MainApp().run()