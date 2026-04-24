"""Composants communs pour les vues."""

from pathlib import Path
import tkinter as tk


def get_asset_path(*parts: str) -> Path:
    """Retourne le chemin absolu vers un asset du projet."""
    base_dir = Path(__file__).resolve().parents[1]
    return base_dir.joinpath(*parts)


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


def center_window(root: tk.Tk, width: int, height: int, resizable: bool = False) -> None:
    """Centre la fenêtre sur l'écran en fonction de la taille donnée."""
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    offset_x = (screen_width - width) // 2
    offset_y = (screen_height - height) // 2
    root.geometry(f"{width}x{height}+{offset_x}+{offset_y}")
    root.resizable(resizable, resizable)
