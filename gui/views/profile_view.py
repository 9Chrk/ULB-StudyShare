"""Vue simple de profil utilisateur (post-login)."""

import tkinter as tk


class ProfileView(tk.Frame):
    """Vue Profile pour tester la navigation via la sidebar."""

    def __init__(self, root, app_controller, bg: str = "#1a1a2e", **kwargs):
        super().__init__(master=root, bg=bg, **kwargs)
        self.app_controller = app_controller

        title = tk.Label(
            self,
            text="Profil",
            font=("Segoe UI", 20, "bold"),
            bg=bg,
            fg="white",
        )
        title.pack(anchor="nw", padx=24, pady=(24, 8))

        subtitle = tk.Label(
            self,
            text="Bienvenue sur ULB StudyShare",
            font=("Segoe UI", 12),
            bg=bg,
            fg="#B0BEC5",
        )
        subtitle.pack(anchor="nw", padx=24)
