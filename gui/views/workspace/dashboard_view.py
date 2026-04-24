"""Vue principale du tableau de bord (post-login)."""

import tkinter as tk


class DashboardView(tk.Frame):
    """Vue Dashboard simple pour illustrer le layout principal."""

    def __init__(self, root, app_controller, bg: str = "#f3f4f6", **kwargs):
        super().__init__(master=root, bg=bg, **kwargs)
        self.app_controller = app_controller

        data = self.app_controller.get_dashboard_data()

        # En-tête du dashboard
        title = tk.Label(
            self,
            text="Dashboard",
            font=("Segoe UI", 20, "bold"),
            bg=bg,
            fg="#111827",
        )
        title.pack(anchor="nw", padx=24, pady=(24, 8))

        subtitle = tk.Label(
            self,
            text=f"Welcome to ULB StudyShare, {data['username']}!",
            font=("Segoe UI", 12),
            bg=bg,
            fg="#6b7280",
        )
        subtitle.pack(anchor="nw", padx=24)
