"""Composants communs pour les vues d'authentification."""

import tkinter as tk


def clear_frames(root: tk.Tk) -> None:
    for widget in root.winfo_children():
        if isinstance(widget, tk.Frame):
            widget.destroy()


def bind_entry_placeholder(entry, placeholder: str, is_password: bool = False) -> None:
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


def center_window(root: tk.Tk, width: int, height: int) -> None:
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    offset_x = (screen_width - width) // 2
    offset_y = (screen_height - height) // 2
    root.geometry(f"{width}x{height}+{offset_x}+{offset_y}")
