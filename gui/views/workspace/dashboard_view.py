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
            text=f"Welcome to ULB StudyShare, {data['profile'].username if data.get('profile') else 'Guest'}!",
            font=("Segoe UI", 12),
            bg=bg,
            fg="#6b7280",
        )
        subtitle.pack(anchor="nw", padx=24)

        profile = self.app_controller.get_profile_data().get("profile")
        if profile is None:
            return
        cards_frame = tk.Frame(self, bg=bg)
        cards_frame.pack(anchor="nw", padx=24, pady=24, fill="x")

        cards = [
            ("Points",  str(profile.points),  "#10b981"),
            ("Level",   str(profile.level),   "#3b82f6"),
        ]

        for label, value, color in cards:
            card = tk.Frame(cards_frame, bg="white", padx=20, pady=16)
            card.pack(side="left", padx=(0, 16))

            tk.Label(card, text=value, font=("Segoe UI", 28, "bold"),
                     bg="white", fg=color).pack()
            tk.Label(card, text=label, font=("Segoe UI", 11),
                     bg="white", fg="#6b7280").pack()
        # Titre actif
        active_title = data.get("active_title")
        tk.Label(
            self,
            text=f"Active title: {active_title if active_title else 'None'}",
            font=("Segoe UI", 11),
            bg=bg, fg="#374151",
        ).pack(anchor="nw", padx=24, pady=(8, 16))

        # Activités récentes
        tk.Label(
            self,
            text="Recent Activity",
            font=("Segoe UI", 14, "bold"),
            bg=bg, fg="#111827",
        ).pack(anchor="nw", padx=24, pady=(0, 8))

        activity = data.get("recent_activity", [])
        if not activity:
            tk.Label(self, text="No recent activity.", bg=bg, fg="#6b7280",
                     font=("Segoe UI", 11)).pack(anchor="nw", padx=24)
        else:
            for act_type, titre, date in activity:
                row = tk.Frame(self, bg="white", padx=12, pady=8)
                row.pack(anchor="nw", padx=24, pady=2, fill="x")
                if act_type == "Published":
                    color = "#68ba9f"
                elif act_type == "Evaluated":
                    color = "#6995dc"
                elif act_type == "Transaction":
                    color = "#f59e0b"
                else:
                    color = "#9ca3af"

                tk.Label(
                    row,
                    text=act_type,
                    font=("Segoe UI", 10, "bold"),
                    bg="white",
                    fg=color,
                    width=10,
                    anchor="w",
                ).pack(side="left")

                tk.Label(
                    row,
                    text=titre,
                    font=("Segoe UI", 10),
                    bg="white",
                    fg="#111827",
                    anchor="w",
                ).pack(side="left", padx=8)

                tk.Label(
                    row,
                    text=str(date),
                    font=("Segoe UI", 9),
                    bg="white",
                    fg="#6b7280",
                    anchor="w",
                ).pack(side="left")

