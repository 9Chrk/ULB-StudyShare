"""Simple post-login My Library view."""

import tkinter as tk


class MyLibraryView(tk.Frame):
    """Simple My Library page for sidebar navigation."""

    def __init__(self, root, app_controller, bg: str = "#1a1a2e", **kwargs):
        super().__init__(master=root, bg=bg, **kwargs)
        self.app_controller = app_controller

        title = tk.Label(
            self,
            text="My Library",
            font=("Segoe UI", 20, "bold"),
            bg=bg,
            fg="white",
        )
        title.pack(anchor="nw", padx=24, pady=(24, 8))

        subtitle = tk.Label(
            self,
            text="Access your saved study materials.",
            font=("Segoe UI", 12),
            bg=bg,
            fg="#B0BEC5",
        )
        subtitle.pack(anchor="nw", padx=24)
