from gui import auth
import tkinter as tk


def run():
    root = tk.Tk()
    auth_app = auth.App(root)
    root.mainloop()
