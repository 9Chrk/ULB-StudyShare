"""Centralise l'affichage des messages GUI."""

from tkinter import messagebox


def show_error(root, message: str) -> None:
    messagebox.showerror("Error", message, parent=root)


def show_info(root, message: str) -> None:
    messagebox.showinfo("Info", message, parent=root)
