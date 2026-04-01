"""Vue d'inscription (construction des widgets et wiring des callbacks)."""

import tkinter as tk
from tkinter import ttk

from gui.ui_helpers import bind_entry_placeholder, clear_frames


def build(root: tk.Tk, on_register, on_login_link) -> dict:
    clear_frames(root)

    register_frame = tk.Frame(root, bg="white", bd=0)
    register_frame.place(relx=0.5, rely=0.5, width=350, height=400, anchor="center")

    close_button = tk.Label(
        register_frame,
        text="×",
        font=("Arial", 16),
        bg="white",
        fg="#999",
        cursor="hand2",
    )
    close_button.place(x=320, y=10)
    close_button.bind("<Button-1>", lambda _: root.destroy())

    title_label = tk.Label(
        register_frame,
        text="Create Account",
        font=("Segoe UI", 20, "bold"),
        bg="white",
    )
    title_label.place(relx=0.5, y=40, anchor="center")

    subtitle_label = tk.Label(
        register_frame,
        text="Join the ULB student community.",
        font=("Segoe UI", 10),
        bg="white",
        fg="#666",
    )
    subtitle_label.place(relx=0.5, y=70, anchor="center")

    user_icon = tk.Label(register_frame, text="👤", font=("Segoe UI", 12), bg="white")
    user_icon.place(x=20, y=110)
    user_entry = ttk.Entry(register_frame, font=("Segoe UI", 10))
    user_entry.insert(0, "Username")
    user_entry.place(x=50, y=110, width=270, height=30)

    email_icon = tk.Label(register_frame, text="📧", font=("Segoe UI", 12), bg="white")
    email_icon.place(x=20, y=160)
    email_entry = ttk.Entry(register_frame, font=("Segoe UI", 10))
    email_entry.insert(0, "Email")
    email_entry.place(x=50, y=160, width=270, height=30)

    password_icon = tk.Label(register_frame, text="🔒", font=("Segoe UI", 12), bg="white")
    password_icon.place(x=20, y=210)
    password_entry = ttk.Entry(register_frame, font=("Segoe UI", 10))
    password_entry.insert(0, "Password")
    password_entry.place(x=50, y=210, width=270, height=30)

    confirm_icon = tk.Label(register_frame, text="🔒", font=("Segoe UI", 12), bg="white")
    confirm_icon.place(x=20, y=260)
    confirm_password_entry = ttk.Entry(register_frame, font=("Segoe UI", 10))
    confirm_password_entry.insert(0, "Confirm Password")
    confirm_password_entry.place(x=50, y=260, width=270, height=30)

    register_button = tk.Button(
        register_frame,
        text="Create Account",
        font=("Segoe UI", 10, "bold"),
        bg="#00d68f",
        fg="white",
        bd=0,
        cursor="hand2",
    )
    register_button.place(x=30, y=310, width=290, height=40)
    register_button.bind(
        "<Button-1>",
        lambda _: on_register(user_entry, password_entry, confirm_password_entry, email_entry),
    )

    login_label = tk.Label(
        register_frame,
        text="Already have an account? ",
        font=("Segoe UI", 9),
        bg="white",
        fg="#999",
    )
    login_label.place(x=70, y=365)

    login_link = tk.Label(
        register_frame,
        text="Log in",
        font=("Segoe UI", 9, "underline"),
        bg="white",
        fg="#00d68f",
        cursor="hand2",
    )
    login_link.place(x=210, y=365)
    login_link.bind("<Button-1>", lambda _: on_login_link())

    bind_entry_placeholder(user_entry, "Username")
    bind_entry_placeholder(email_entry, "Email")
    bind_entry_placeholder(password_entry, "Password", is_password=True)
    bind_entry_placeholder(confirm_password_entry, "Confirm Password", is_password=True)

    return {
        "user_entry": user_entry,
        "email_entry": email_entry,
        "password_entry": password_entry,
        "confirm_password_entry": confirm_password_entry,
    }
