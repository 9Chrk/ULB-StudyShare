"""Vue simple de profil utilisateur (post-login)."""

import tkinter as tk


class ProfileView(tk.Frame):
    """Vue Profile pour tester la navigation via la sidebar."""

    def __init__(self, root, app_controller, bg: str = "#f3f4f6", **kwargs):
        super().__init__(master=root, bg=bg, **kwargs)
        self.app_controller = app_controller

        title = tk.Label(
            self,
            text="Profile",
            font=("Segoe UI", 20, "bold"),
            bg=bg,
            fg="#111827",
        )
        title.pack(anchor="nw", padx=24, pady=(24, 8))

        subtitle = tk.Label(
            self,
            text="View and edit your profile information.",
            font=("Segoe UI", 12),
            bg=bg,
            fg="#6b7280",
        )
        subtitle.pack(anchor="nw", padx=24)
    

    # Data
        data = self.app_controller.get_profile_data()
        profile = data.get("profile")

        if profile is None:
            tk.Label(self, text="No profile found.", bg=bg, fg="#ef4444").pack(padx=24, pady=16)
            return

        card = tk.Frame(self, bg="white", padx=24, pady=24)
        card.pack(anchor="nw", padx=24, pady=16, fill="x")

        fields = [
            ("Username",     profile.username),
            ("Email",        profile.email),
            ("Member since", str(profile.registration_date)),
            ("Level",        str(profile.level)),
            ("Points",       str(profile.points)),
        ]

        for label, value in fields:
            row = tk.Frame(card, bg="white")
            row.pack(anchor="w", pady=6, fill="x")
            tk.Label(row, text=label, font=("Segoe UI", 11, "bold"),
                     bg="white", fg="#374151", width=15, anchor="w").pack(side="left")
            tk.Label(row, text=value, font=("Segoe UI", 11),
                     bg="white", fg="#111827", anchor="w").pack(side="left")
