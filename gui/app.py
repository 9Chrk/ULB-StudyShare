"""Point d'entrée de l'application GUI."""

import tkinter as tk

from gui.controller import AppController
from gui.ui_setup import configure_root


def run():
    """Initialise la fenêtre principale et lance la boucle Tkinter."""
    root = tk.Tk()
    configure_root(root)
    AppController(root)
    root.mainloop()
