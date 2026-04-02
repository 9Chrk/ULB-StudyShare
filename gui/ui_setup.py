"""Configuration de la fenêtre principale Tkinter."""

import tkinter as tk
from tkinter import font, ttk


def configure_root(root: tk.Tk) -> None:
    """Configure la fenêtre racine (titre, thème et styles globaux)."""
    
    root.title("ULB StudyShare")
    root.configure(bg="#1a1a2e")
    center_window(root, width=500, height=600)

    default_font = font.nametofont("TkDefaultFont")
    default_font.configure(family="Segoe UI", size=10)

    style = ttk.Style()
    style.configure("TLabel", font=("Segoe UI", 10))
    style.configure("TButton", font=("Segoe UI", 10))
    style.configure("TEntry", font=("Segoe UI", 10))


# ---------- FONCTIONS UTILITAIRES ---------

def center_window(root: tk.Tk, width: int, height: int) -> None:
    """Centre la fenêtre sur l'écran en fonction de la taille donnée."""
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    offset_x = (screen_width - width) // 2
    offset_y = (screen_height - height) // 2
    root.geometry(f"{width}x{height}+{offset_x}+{offset_y}")
    root.resizable(False, False)
