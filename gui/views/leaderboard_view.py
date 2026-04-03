"""Simple post-login Leaderboard view."""

import tkinter as tk


class LeaderboardView(tk.Frame):
    """Simple Leaderboard page for sidebar navigation."""

    def __init__(self, root, app_controller, bg: str = "#1a1a2e", **kwargs):
        super().__init__(master=root, bg=bg, **kwargs)
        self.app_controller = app_controller

        title = tk.Label(
            self,
            text="Leaderboard",
            font=("Segoe UI", 20, "bold"),
            bg=bg,
            fg="white",
        )
        title.pack(anchor="nw", padx=24, pady=(24, 8))

        subtitle = tk.Label(
            self,
            text="See top contributors in the community.",
            font=("Segoe UI", 12),
            bg=bg,
            fg="#B0BEC5",
        )
        subtitle.pack(anchor="nw", padx=24)
