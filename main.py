import flet as ft
from flet import TextField, Checkbox, ElevatedButton, Text, Row, Column
from flet_core.control_event import ControlEvent
from flet import (UserControl, InputBorder, Page)
from hashlib import sha256



class TextEditor(UserControl):
    def __init__(self, username, text_password) -> None:
        UserControl.__init__(self)  # Call the constructor of UserControl
        self.username = username
        self.text_password = text_password
        self.textfile = f'{self.username}_{sha256(self.text_password.value.encode("UTF-8")).hexdigest()}_save.txt'
        self.textfield = TextField(multiline=True,
                                   autofocus=True,
                                   border=InputBorder.NONE,
                                   min_lines=40,
                                   on_change=self.save_text,
                                   content_padding=30,
                                   cursor_color='yellow')

    # Rest of the class remains the same

    def save_text(self, e: ControlEvent):
        with open(self.textfile, 'w') as f:
            f.write(self.textfield.value)

    def read_text(self) -> str or None:
        try:
            with open(self.textfile, 'r') as f:
                return f.read()
        except FileNotFoundError:
            self.textfield.hint_text = 'Welcome To Editor Pro. Type something to get started!'

    def build(self) -> TextField:
        self.textfield.value = self.read_text()
        return self.textfield


def main_logged_in_page(page: Page, username: str, password: str) -> None:
    page.title = 'Editor Pro Edition.'
    page.scroll = True

    # Create a TextEditor for the current user
    text_editor = TextEditor(username, password)
    page.add(text_editor)


# Function to save user data in logins.txt
def save_user_data(username, password):
    with open("logins.txt", "a") as file:
        file.write(f"Username: {username}, Password: {password}\n")


# Function to check if a user is in logins.txt
def is_user_in_logins(username, password):
    with open("logins.txt", "r") as file:
        for line in file:
            if f"Username: {username}, Password: {password}" in line:
                return True
    return False


def main(page: ft.Page) -> None:
    page.title = 'Signup'
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window_width = 400
    page.window_height = 400
    page.window_resizable = True

    def redirect_to_login(e: ControlEvent) -> None:
        page.clean()
        login_page()

    def login_page():
        page.title = 'Login'
        page.clean()
        page.add(
            Row(
                controls=[Text(value="Enter your credentials", size=20)],
                alignment=ft.MainAxisAlignment.CENTER
            )
        )

        # Login Text fields
        login_username: TextField = TextField(label='Username', text_align=ft.TextAlign.LEFT, width=200)
        login_password: TextField = TextField(label='Password', text_align=ft.TextAlign.LEFT, width=200, password=True)
        button_login: ElevatedButton = ElevatedButton(text='Log in', width=200, disabled=True)

        def validate_login(e: ControlEvent) -> None:
            if all([login_username.value, login_password.value]):
                button_login.disabled = False
            else:
                button_login.disabled = True

            page.update()

        def log_in(e: ControlEvent) -> None:
            username = login_username.value
            password = login_password.value

            if is_user_in_logins(username, password):
                page.clean()
                main_logged_in_page(page, username, password.value)  # Pass the 'page' parameter here
            else:
                page.clean()
                page.add(
                    Row(
                        controls=[Text(value="Login failed. Please try again.", size=20)],
                        alignment=ft.MainAxisAlignment.CENTER
                    )
                )

        button_login.on_click = log_in
        login_username.on_change = validate_login
        login_password.on_change = validate_login

        page.add(
            Row(
                controls=[
                    Column(
                        [login_username,
                         login_password,
                         button_login]
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER
            )
        )

    # Create the "Login" button
    button_login_redirect: ElevatedButton = ElevatedButton(text='Login', width=100)
    button_login_redirect.on_click = redirect_to_login
    page.add(
        Row(
            controls=[
                Column(
                    [button_login_redirect]
                )
            ],
            alignment=ft.MainAxisAlignment.START
        )
    )

    # Set up our Text fields, Checkbox, Button for Sign Up
    text_username: TextField = TextField(label='Username', text_align=ft.TextAlign.LEFT, width=200)
    text_password: TextField = TextField(label='Password', text_align=ft.TextAlign.LEFT, width=200, password=True)
    checkbox_signup: Checkbox = Checkbox(label="Do you agree to Editor PRO's \n Terms of Conditions?", value=False)
    button_submit: ElevatedButton = ElevatedButton(text='Sign up', width=200, disabled=True)

    def validate(e: ControlEvent) -> None:
        if all([text_username.value, text_password.value, checkbox_signup.value]):
            button_submit.disabled = False
        else:
            button_submit.disabled = True

        page.update()

    def submit(e: ControlEvent) -> None:
        username = text_username.value
        password = text_password.value
        save_user_data(username, password)

        page.clean()
        main_logged_in_page(page, username, text_password)

    checkbox_signup.on_change = validate
    text_username.on_change = validate
    text_password.on_change = validate
    button_submit.on_click = submit

    # Render the sign-up page
    page.add(
        Row(
            controls=[
                Column(
                    [text_username,
                     text_password,
                     checkbox_signup,
                     button_submit]
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER
        )
    )


if __name__ == "__main__":
    ft.app(target=main)
