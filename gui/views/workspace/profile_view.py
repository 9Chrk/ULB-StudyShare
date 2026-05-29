"""Vue simple de profil utilisateur (post-login)."""

import tkinter as tk
from tkinter import ttk

import gui.views.common.theme as theme


class ProfileView(tk.Frame):
    """Vue Profil affichant les informations du compte connecté."""

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
            text="Consultez les informations de votre profil.",
            font=("Segoe UI", 12),
            bg=bg,
            fg=theme.WORKSPACE_MUTED,
        ).pack(anchor="nw", padx=24)

        self.content_frame = tk.Frame(self, bg=bg)
        self.content_frame.pack(fill="both", expand=True)

    def refresh(self) -> None:
        """Recharge les informations du profil."""
        data = self.app_controller.get_profile_data()

        for child in self.content_frame.winfo_children():
            child.destroy()

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

        self._build_transaction_history(data.point_transactions)

    # --------------------------------------------------------
    # Méthodes de rendu
    # --------------------------------------------------------

    def _build_transaction_history(self, transactions) -> None:
        """Affiche l'historique récent des transactions de points."""
        history_card = tk.Frame(
            self.content_frame,
            bg=theme.COLORS.white,
            padx=24,
            pady=18,
            highlightbackground=theme.WORKSPACE_BORDER,
            highlightthickness=1,
        )
        history_card.pack(anchor="nw", padx=24, pady=(0, 16), fill="x")

        tk.Label(
            history_card,
            text="Historique des transactions de points",
            font=("Segoe UI", 13, "bold"),
            bg=theme.COLORS.white,
            fg=theme.WORKSPACE_TEXT,
        ).pack(anchor="w")

        tk.Label(
            history_card,
            text="Les 20 dernières opérations enregistrées sur votre solde.",
            font=("Segoe UI", 9),
            bg=theme.COLORS.white,
            fg=theme.WORKSPACE_MUTED,
        ).pack(anchor="w", pady=(2, 10))

        if not transactions:
            tk.Label(
                history_card,
                text="Aucune transaction de points pour le moment.",
                font=("Segoe UI", 10),
                bg=theme.COLORS.white,
                fg=theme.WORKSPACE_MUTED,
            ).pack(anchor="w")
            return

        table_frame = tk.Frame(history_card, bg=theme.COLORS.white)
        table_frame.pack(fill="x")

        columns = ("date", "nature", "motif", "montant")
        tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            height=min(len(transactions), 8),
        )
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        tree.heading("date", text="Date")
        tree.heading("nature", text="Type")
        tree.heading("motif", text="Motif")
        tree.heading("montant", text="Points")

        tree.column("date", width=150, anchor="w")
        tree.column("nature", width=90, anchor="center")
        tree.column("motif", width=360, anchor="w")
        tree.column("montant", width=80, anchor="center")

        for transaction in transactions:
            is_gain = transaction.nature == "gain"
            nature = "Gain" if is_gain else "Dépense"
            sign = "+" if is_gain else "-"
            tree.insert(
                "",
                "end",
                values=(
                    transaction.transaction_date,
                    nature,
                    transaction.reason,
                    f"{sign}{transaction.amount}",
                ),
            )

        tree.pack(side="left", fill="x", expand=True)
        scrollbar.pack(side="right", fill="y")
