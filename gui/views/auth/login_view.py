"""Vue de connexion (construction des widgets et wiring des callbacks)."""

import tkinter as tk
from tkinter import ttk

from gui.ui_helpers import bind_entry_placeholder, clear_frames, get_asset_path


def build(root: tk.Tk, on_login, on_register_link) -> dict:
    """Construit la vue de connexion et branche les callbacks de l'application."""
    # -------- Reset --------
    # Nettoyer la fenêtre avant d'afficher la vue de connexion
    clear_frames(root)

    # -------- Branding --------
    # Charger le logo de l'application
    logo_image = tk.PhotoImage(
        file=str(get_asset_path("assets", "images", "ulb_logo.png"))
    ).subsample(10, 10)

    # Frame principale blanche, centrée dans la fenêtre
    login_frame = tk.Frame(root, bg="white", bd=0)
    login_frame.place(relx=0.5, rely=0.5, width=350, height=320, anchor="center")

    # -------- Header --------
    # Bouton de fermeture (croix en haut à droite)
    close_button = tk.Label(
        login_frame,
        text="×",
        font=("Arial", 16),
        bg="white",
        fg="#999",
        cursor="hand2",
    )
    close_button.place(x=320, y=10)
    close_button.bind("<Button-1>", lambda _: root.destroy())

    # Logo + titre principal de l'application
    logo_label = tk.Label(login_frame, image=logo_image, bg="white")
    logo_label.place(x=45, y=20)
    login_frame.logo_image = logo_image

    title_label = tk.Label(
        login_frame,
        text="StudyShare",
        font=("Segoe UI", 20, "bold"),
        bg="white",
    )
    title_label.place(x=100, y=20)

    # Sous-titre (slogan) sous le titre principal
    subtitle_label = tk.Label(
        login_frame,
        text="Share. Learn. Grow.",
        font=("Segoe UI", 10),
        bg="white",
        fg="#666",
    )
    subtitle_label.place(relx=0.5, y=70, anchor="center")

    # -------- Fields --------
    # Icône + champ de saisie pour le nom d'utilisateur
    user_icon = tk.Label(login_frame, text="👤", font=("Segoe UI", 12), bg="white")
    user_icon.place(x=20, y=110)
    user_entry = ttk.Entry(login_frame, font=("Segoe UI", 10))
    user_entry.insert(0, "Username")
    user_entry.place(x=50, y=110, width=270, height=30)

    # Icône + champ de saisie pour le mot de passe
    password_icon = tk.Label(login_frame, text="🔒", font=("Segoe UI", 12), bg="white")
    password_icon.place(x=20, y=160)
    password_entry = ttk.Entry(login_frame, font=("Segoe UI", 10))
    password_entry.insert(0, "Password")
    password_entry.place(x=50, y=160, width=270, height=30)

    # -------- Actions --------
    # Bouton qui déclenche la tentative de connexion
    login_button = tk.Button(
        login_frame,
        text="Log in",
        font=("Segoe UI", 10, "bold"),
        bg="#00d68f",
        fg="white",
        bd=0,
        cursor="hand2",
    )
    login_button.place(x=30, y=210, width=290, height=40)
    login_button.bind("<Button-1>", lambda _: on_login(user_entry, password_entry))

    # Texte + lien cliquable pour naviguer vers l'inscription
    register_label = tk.Label(
        login_frame,
        text="New user? ",
        font=("Segoe UI", 9),
        bg="white",
        fg="#999",
    )
    register_label.place(x=70, y=270)

    register_link = tk.Label(
        login_frame,
        text="Create an account",
        font=("Segoe UI", 9, "underline"),
        bg="white",
        fg="#00d68f",
        cursor="hand2",
    )
    register_link.place(x=130, y=270)
    register_link.bind("<Button-1>", lambda _: on_register_link())

    # -------- Placeholders --------
    # Gestion des placeholders et masquage du mot de passe
    bind_entry_placeholder(user_entry, "Username")
    bind_entry_placeholder(password_entry, "Password", is_password=True)

    return {"user_entry": user_entry, "password_entry": password_entry}
