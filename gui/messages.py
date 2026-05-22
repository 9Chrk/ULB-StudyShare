"""Centralise l'affichage des messages GUI."""

from tkinter import messagebox


def show_error(root, message: str) -> None:
    """Affiche une boîte de dialogue d'erreur modale."""
    messagebox.showerror("Erreur", message, parent=root)


def show_info(root, message: str) -> None:
    """Affiche une boîte de dialogue d'information modale."""
    messagebox.showinfo("Info", message, parent=root)
