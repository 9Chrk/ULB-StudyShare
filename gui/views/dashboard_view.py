"""Vue principale du tableau de bord (post-login)."""

import tkinter as tk


class DashboardView(tk.Frame):
    """Vue Dashboard simple pour illustrer le layout principal."""

    def __init__(self, root, app_controller, bg: str = "#1a1a2e", **kwargs):
        super().__init__(master=root, bg=bg, **kwargs)
        self.app_controller = app_controller

        # En-tête du dashboard
        title = tk.Label(
            self,
            text="Dashboard",
            font=("Segoe UI", 20, "bold"),
            bg="#1a1a2e",
            fg="white",
        )
        title.pack(anchor="nw", padx=24, pady=(24, 8))

        subtitle = tk.Label(
            self,
            text="Welcome to ULB StudyShare",
            font=("Segoe UI", 12),
            bg="#1a1a2e",
            fg="#B0BEC5",
        )
        subtitle.pack(anchor="nw", padx=24)
