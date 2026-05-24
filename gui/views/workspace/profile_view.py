"""Vue simple de profil utilisateur (post-login)."""

import tkinter as tk

import gui.views.common.theme as theme


class ProfileView(tk.Frame):
    """Vue Profil pour tester la navigation via la sidebar."""

    def __init__(
        self, root, app_controller, bg: str = theme.WORKSPACE_BACKGROUND, **kwargs
    ):
        """Construit la vue Profil et affiche les informations de l'utilisateur."""
        super().__init__(master=root, bg=bg, **kwargs)
        self.app_controller = app_controller
        self.bg = bg

        # -------- Header --------
        tk.Label(
            self,
            text="Profil",
            font=("Segoe UI", 20, "bold"),
            bg=bg,
            fg=theme.WORKSPACE_TEXT,
        ).pack(anchor="nw", padx=24, pady=(24, 8))

        tk.Label(
            self,
            text="Consultez et modifiez les informations de votre profil.",
            font=("Segoe UI", 12),
            bg=bg,
            fg=theme.WORKSPACE_MUTED,
        ).pack(anchor="nw", padx=24)

        self.content_frame = tk.Frame(self, bg=bg)
        self.content_frame.pack(fill="both", expand=True)

        self.refresh()

    def refresh(self) -> None:
        """Recharge les informations du profil."""
        for child in self.content_frame.winfo_children():
            child.destroy()

        data = self.app_controller.get_profile_data()
        profile = data.profile

        if profile is None:
            # -------- Empty state --------
            tk.Label(
                self.content_frame,
                text="Aucun profil trouvé.",
                bg=self.bg,
                fg=theme.WORKSPACE_RED,
            ).pack(padx=24, pady=16)
            return

        # -------- Details card --------
        card = tk.Frame(self.content_frame, bg=theme.COLORS.white, padx=24, pady=24)
        card.pack(anchor="nw", padx=24, pady=16, fill="x")

        # -------- Fields --------
        fields = [
            ("Nom d'utilisateur", profile.username),
            ("E-mail", profile.email),
            ("Membre depuis", str(profile.registration_date)),
            ("Niveau", str(profile.level)),
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
