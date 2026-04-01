"""Composants communs pour les vues."""

import tkinter as tk


def clear_frames(root: tk.Tk) -> None:
    """Supprime tous les widgets Frame présents dans la fenêtre racine."""
    for widget in root.winfo_children():
        if isinstance(widget, tk.Frame):
            widget.destroy()


def bind_entry_placeholder(entry, placeholder: str, is_password: bool = False) -> None:
    """Ajoute un placeholder géré au focus sur un champ de saisie."""
    
    def focus_in(_event):
        if entry.get() == placeholder:
            entry.delete(0, tk.END)
            if is_password:
                entry.config(show="•")

    def focus_out(_event):
        if entry.get() == "":
            entry.insert(0, placeholder)
            if is_password:
                entry.config(show="")

    entry.bind("<FocusIn>", focus_in)
    entry.bind("<FocusOut>", focus_out)
