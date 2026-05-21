"""Vue simple de profil utilisateur (post-login)."""

import tkinter as tk

import gui.views.common.theme as theme


class ProfileView(tk.Frame):
    """Vue Profile pour tester la navigation via la sidebar."""

    def __init__(
        self, root, app_controller, bg: str = theme.WORKSPACE_BACKGROUND, **kwargs
    ):
        super().__init__(master=root, bg=bg, **kwargs)
        self.app_controller = app_controller

        title = tk.Label(
            self,
            text="Profile",
            font=("Segoe UI", 20, "bold"),
            bg=bg,
            fg=theme.WORKSPACE_TEXT,
        )
        title.pack(anchor="nw", padx=24, pady=(24, 8))

        subtitle = tk.Label(
            self,
            text="View and edit your profile information.",
            font=("Segoe UI", 12),
            bg=bg,
            fg=theme.WORKSPACE_MUTED,
        )
        subtitle.pack(anchor="nw", padx=24)

        # Data
        data = self.app_controller.get_profile_data()
        profile = data.profile

        if profile is None:
            tk.Label(
                self, text="No profile found.", bg=bg, fg=theme.WORKSPACE_RED
            ).pack(padx=24, pady=16)
            return

        card = tk.Frame(self, bg=theme.COLORS.white, padx=24, pady=24)
        card.pack(anchor="nw", padx=24, pady=16, fill="x")

        fields = [
            ("Username", profile.username),
            ("Email", profile.email),
            ("Member since", str(profile.registration_date)),
            ("Level", str(profile.level)),
            ("Points", str(profile.points)),
        ]

        for label, value in fields:
            row = tk.Frame(card, bg=theme.COLORS.white)
            row.pack(anchor="w", pady=6, fill="x")
            tk.Label(
                row,
                text=label,
                font=("Segoe UI", 11, "bold"),
                bg=theme.COLORS.white,
                fg=theme.WORKSPACE_TEXT,
                width=15,
                anchor="w",
            ).pack(side="left")
            tk.Label(
                row,
                text=value,
                font=("Segoe UI", 11),
                bg=theme.COLORS.white,
                fg=theme.WORKSPACE_TEXT,
                anchor="w",
            ).pack(side="left")
