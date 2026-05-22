"""Vue principale du tableau de bord (post-login)."""

import tkinter as tk

import gui.views.common.theme as theme


class DashboardView(tk.Frame):
    """Vue du tableau de bord simple pour illustrer le layout principal."""

    def __init__(
        self, root, app_controller, bg: str = theme.WORKSPACE_BACKGROUND, **kwargs
    ):
        """Construit le tableau de bord et peuple les cartes de synthèse."""
        super().__init__(master=root, bg=bg, **kwargs)
        self.app_controller = app_controller

        data = self.app_controller.get_dashboard_data()

        # -------- Header --------
        # En-tête du tableau de bord
        title = tk.Label(
            self,
            text="Dashboard",
            font=("Segoe UI", 20, "bold"),
            bg=bg,
            fg=theme.WORKSPACE_TEXT,
        )
        title.pack(anchor="nw", padx=24, pady=(24, 8))

        subtitle = tk.Label(
            self,
            text=f"Welcome to ULB StudyShare, {data.profile.username if data.profile else 'Guest'}!",
            font=("Segoe UI", 12),
            bg=bg,
            fg=theme.WORKSPACE_MUTED,
        )
        subtitle.pack(anchor="nw", padx=24)

        # -------- Résumé du profil --------
        profile = data.profile
        if profile is None:
            # Sans profil chargé, on garde l'en-tête et on stoppe l'affichage détaillé.
            return
        cards_frame = tk.Frame(self, bg=bg)
        cards_frame.pack(anchor="nw", padx=24, pady=24, fill="x")

        cards = [
            ("Points", str(profile.points), theme.COLORS.black),
            ("Level", str(profile.level), theme.COLORS.gray_500),
        ]

        for label, value, color in cards:
            card = tk.Frame(cards_frame, bg=theme.COLORS.white, padx=20, pady=16)
            card.pack(side="left", padx=(0, 16))

            tk.Label(
                card,
                text=value,
                font=("Segoe UI", 28, "bold"),
                bg=theme.COLORS.white,
                fg=color,
            ).pack()
            tk.Label(
                card,
                text=label,
                font=("Segoe UI", 11),
                bg=theme.COLORS.white,
                fg=theme.WORKSPACE_MUTED,
            ).pack()
        # Titre actif
        active_title = data.active_title
        # Le titre actif peut être absent tant qu'aucun objet n'est activé.
        tk.Label(
            self,
            text=f"Active title: {active_title if active_title else 'None'}",
            font=("Segoe UI", 11),
            bg=bg,
            fg=theme.WORKSPACE_NEUTRAL_TEXT,
        ).pack(anchor="nw", padx=24, pady=(8, 16))

        # Activités récentes
        tk.Label(
            self,
            text="Recent Activity",
            font=("Segoe UI", 14, "bold"),
            bg=bg,
            fg=theme.WORKSPACE_TEXT,
        ).pack(anchor="nw", padx=24, pady=(0, 8))

        activity = data.recent_activity
        if not activity:
            tk.Label(
                self,
                text="No recent activity.",
                bg=bg,
                fg=theme.WORKSPACE_MUTED,
                font=("Segoe UI", 11),
            ).pack(anchor="nw", padx=24)
        else:
            for item in activity:
                row = tk.Frame(self, bg=theme.COLORS.white, padx=12, pady=8)
                row.pack(anchor="nw", padx=24, pady=2, fill="x")
                
                # Chaque type d'activité garde une couleur lisible et cohérente.
                if item.activity_type == "Published":
                    color = theme.WORKSPACE_GREEN
                elif item.activity_type == "Evaluated":
                    color = theme.WORKSPACE_BLUE_LIGHT
                elif item.activity_type == "Transaction":
                    color = theme.WORKSPACE_ORANGE
                else:
                    color = theme.WORKSPACE_MUTED

                tk.Label(
                    row,
                    text=item.activity_type,
                    font=("Segoe UI", 10, "bold"),
                    bg=theme.COLORS.white,
                    fg=color,
                    width=10,
                    anchor="w",
                ).pack(side="left")

                tk.Label(
                    row,
                    text=item.title,
                    font=("Segoe UI", 10),
                    bg=theme.COLORS.white,
                    fg=theme.WORKSPACE_TEXT,
                    anchor="w",
                ).pack(side="left", padx=8)

                tk.Label(
                    row,
                    text=str(item.activity_date),
                    font=("Segoe UI", 9),
                    bg=theme.COLORS.white,
                    fg=theme.WORKSPACE_MUTED,
                    anchor="w",
                ).pack(side="left")
