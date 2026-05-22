"""Vue du classement simple après connexion."""

import tkinter as tk
from tkinter import ttk

import gui.views.common.theme as theme


class LeaderboardView(tk.Frame):
    """Vue dédiée au classement des utilisateurs par points."""

    def __init__(
        self, root, app_controller, bg: str = theme.WORKSPACE_BACKGROUND, **kwargs
    ):
        """Construit la vue du classement et remplit le tableau des joueurs."""
        super().__init__(master=root, bg=bg, **kwargs)
        self.app_controller = app_controller

        data = self.app_controller.get_leaderboard_data()

        # -------- Header --------
        # Titre
        tk.Label(
            self,
            text="Leaderboard",
            font=("Segoe UI", 20, "bold"),
            bg=bg,
            fg=theme.WORKSPACE_TEXT,
        ).pack(anchor="nw", padx=24, pady=(24, 8))

        tk.Label(
            self,
            text="See top contributors in the community.",
            font=("Segoe UI", 12),
            bg=bg,
            fg=theme.WORKSPACE_MUTED,
        ).pack(anchor="nw", padx=24, pady=(0, 16))

        # -------- Tableau du classement --------
        # Tableau avec barre de défilement
        frame = tk.Frame(self, bg=bg)
        frame.pack(fill="both", expand=True, padx=24, pady=(0, 16))

        columns = ("rang", "username", "points", "niveau")
        tree = ttk.Treeview(frame, columns=columns, show="headings", height=12)

        tree.heading("rang", text="Rank")
        tree.heading("username", text="Player")
        tree.heading("points", text="Points")
        tree.heading("niveau", text="Level")

        tree.column("rang", width=50, anchor="center")
        tree.column("username", width=150, anchor="w")
        tree.column("points", width=80, anchor="center")
        tree.column("niveau", width=60, anchor="center")

        # Barre de défilement
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)

        # -------- Rows --------
        # Remplissage
        current_user = data.current_username
        leaderboard = data.entries

        current_user_rank = None
        for i, entry in enumerate(leaderboard, start=1):
            # On marque la ligne de l'utilisateur courant pour la mettre en évidence.
            tag = "current" if entry.username == current_user else ""
            if entry.username == current_user:
                current_user_rank = i
            tree.insert(
                "",
                "end",
                values=(i, entry.username, entry.points, entry.level),
                tags=(tag,),
            )

        tree.tag_configure("current", background=theme.WORKSPACE_HIGHLIGHT)

        scrollbar.pack(side="right", fill="y")
        tree.pack(side="left", fill="both", expand=True)

        # -------- Panneau de position --------
        # Espace vide
        tk.Frame(self, bg=bg, height=12).pack(fill="x")

        # Panel position utilisateur (en bas)
        user_panel = tk.Frame(
            self, bg=theme.COLORS.white, relief="solid", borderwidth=1
        )
        user_panel.pack(fill="x", padx=24, pady=(0, 24))

        content_frame = tk.Frame(user_panel, bg=theme.COLORS.white)
        content_frame.pack(fill="both", expand=True, padx=12, pady=12)

        tk.Label(
            content_frame,
            text="Your Position",
            font=("Segoe UI", 11, "bold"),
            bg=theme.COLORS.white,
            fg=theme.WORKSPACE_MUTED,
        ).pack(anchor="w")

        if current_user_rank:
            # Le rang est calculé en local pour éviter de dépendre d'un champ dédié.
            position_text = f"Rank #{current_user_rank} - {current_user}"
        else:
            position_text = f"Not ranked - {current_user}"

        tk.Label(
            content_frame,
            text=position_text,
            font=("Segoe UI", 13, "bold"),
            bg=theme.COLORS.white,
            fg=theme.WORKSPACE_GREEN,
        ).pack(anchor="w", pady=(4, 0))
