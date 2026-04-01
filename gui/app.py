"""Contrôleur de l'authentification GUI."""

from tkinter import font, ttk

from core import auth_service
from gui import messages
from gui.views import login_view, register_view
from gui.views.common import center_window


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("ULB StudyShare")
        center_window(root, width=500, height=600)

        default_font = font.nametofont("TkDefaultFont")
        default_font.configure(family="Segoe UI", size=10)

        style = ttk.Style()
        style.configure("TLabel", font=("Segoe UI", 10))
        style.configure("TButton", font=("Segoe UI", 10))
        style.configure("TEntry", font=("Segoe UI", 10))

        self.root.configure(bg="#1a1a2e")
        self.login_menu()

    def login_menu(self):
        login_view.build(
            root=self.root,
            on_login=self.login,
            on_register_link=self.register_menu,
        )

    def register_menu(self):
        register_view.build(
            root=self.root,
            on_register=self.register,
            on_login_link=self.login_menu,
        )

    def login(self, user_entry, password_entry):
        username = user_entry.get()
        password = password_entry.get()

        password_entry.delete(0, "end")
        is_ok, message = auth_service.check(username, password)

        if is_ok:
            user_entry.delete(0, "end")
            messages.show_info(self.root, "Login successful!")
        else:
            messages.show_error(self.root, message)

    def register(self, user_entry, password_entry, confirm_password_entry, email_entry):
        username = user_entry.get()
        email = email_entry.get()
        password = password_entry.get()
        confirm_password = confirm_password_entry.get()

        password_entry.delete(0, "end")
        confirm_password_entry.delete(0, "end")

        if password != confirm_password:
            messages.show_error(self.root, "Passwords do not match.")
            return

        is_ok, message = auth_service.add(username, password, email)
        
        if is_ok:
            user_entry.delete(0, "end")
            email_entry.delete(0, "end")
            messages.show_info(self.root, "Registration successful!")
            self.login_menu()
        else:
            messages.show_error(self.root, message)
