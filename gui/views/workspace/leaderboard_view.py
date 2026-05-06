"""Simple post-login Leaderboard view."""
import tkinter as tk
from tkinter import ttk


class LeaderboardView(tk.Frame):

    def __init__(self, root, app_controller, bg: str = "#f3f4f6", **kwargs):
        super().__init__(master=root, bg=bg, **kwargs)
        self.app_controller = app_controller

        data = self.app_controller.get_leaderboard_data()

        # Titre
        tk.Label(
            self,
            text="Leaderboard",
            font=("Segoe UI", 20, "bold"),
            bg=bg, fg="#111827",
        ).pack(anchor="nw", padx=24, pady=(24, 8))

        tk.Label(
            self,
            text="Top 10 des utilisateurs par points",
            font=("Segoe UI", 12),
            bg=bg, fg="#6b7280",
        ).pack(anchor="nw", padx=24, pady=(0, 16))

        # Tableau
        frame = tk.Frame(self, bg=bg)
        frame.pack(fill="both", expand=True, padx=24)

        columns = ("rang", "username", "points", "niveau")
        tree = ttk.Treeview(frame, columns=columns, show="headings", height=10)

        tree.heading("rang",     text="Rang")
        tree.heading("username", text="Utilisateur")
        tree.heading("points",   text="Points")
        tree.heading("niveau",   text="Niveau")

        tree.column("rang",     width=60,  anchor="center")
        tree.column("username", width=200, anchor="w")
        tree.column("points",   width=100, anchor="center")
        tree.column("niveau",   width=80,  anchor="center")

        # Remplissage
        current_user = data.get("user_id")
        for i, (username, points, niveau) in enumerate(data["leaderboard"], start=1):
            tag = "current" if username == current_user else ""
            tree.insert("", "end",
                        values=(i, username, points, niveau),
                        tags=(tag,))

        tree.tag_configure("current", background="#d1fae5")  # vert clair pour l'utilisateur courant
        tree.pack(fill="both", expand=True)
