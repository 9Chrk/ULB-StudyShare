"""Simple post-login Explorer view."""

import tkinter as tk


class ExplorerView(tk.Frame):
    """Simple Explorer page for sidebar navigation."""

    def __init__(self, root, app_controller, bg: str = "#f3f4f6", **kwargs):
        super().__init__(master=root, bg=bg, **kwargs)
        self.app_controller = app_controller

        title = tk.Label(
            self,
            text="Explorer",
            font=("Segoe UI", 20, "bold"),
            bg=bg,
            fg="#111827",
        )
        title.pack(anchor="nw", padx=24, pady=(24, 8))

        subtitle = tk.Label(
            self,
            text="Discover courses and new resources.",
            font=("Segoe UI", 12),
            bg=bg,
            fg="#6b7280",
        )
        subtitle.pack(anchor="nw", padx=24)
