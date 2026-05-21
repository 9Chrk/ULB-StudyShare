"""Configuration de la fenêtre principale Tkinter."""

import tkinter as tk
from tkinter import font, ttk
from gui.ui_helpers import center_window, get_asset_path


def configure_root(root: tk.Tk) -> None:
    """Configure la fenêtre racine."""

    # Configurer le titre, l'icône et le thème de la fenêtre principale
    root.title("ULB StudyShare")
    root.configure(bg="#1a1a2e")
    window_icon = tk.PhotoImage(
        file=str(get_asset_path("assets", "images", "ulb_logo.png"))
    )
    root._window_icon = window_icon
    root.iconphoto(True, window_icon)
    center_window(root, width=1280, height=720, resizable=False)

    # Configurer la police par défaut pour toute l'application
    default_font = font.nametofont("TkDefaultFont")
    default_font.configure(family="Segoe UI", size=10)

    # Configurer les styles globaux pour les widgets ttk
    style = ttk.Style()
    style.configure("TLabel", font=("Segoe UI", 10))
    style.configure("TButton", font=("Segoe UI", 10))
    style.configure("TEntry", font=("Segoe UI", 10))
