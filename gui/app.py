import tkinter as tk

from gui.controller import AppController
from gui.ui_setup import configure_root


def run():
    root = tk.Tk()
    configure_root(root)
    AppController(root)
    root.mainloop()
