"""Vue Bibliothèque personnelle simple après connexion."""

import tkinter as tk

import gui.views.common.theme as theme


class MyLibraryView(tk.Frame):
    """Page Bibliothèque personnelle simple pour la navigation latérale."""

    def __init__(
        self, root, app_controller, bg: str = theme.WORKSPACE_BACKGROUND, **kwargs
    ):
        """Construit la vue Bibliothèque personnelle."""
        super().__init__(master=root, bg=bg, **kwargs)
        self.app_controller = app_controller

        # -------- Header --------
        title = tk.Label(
            self,
            text="Ma bibliothèque",
            font=("Segoe UI", 20, "bold"),
            bg=bg,
            fg=theme.WORKSPACE_TEXT,
        )
        title.pack(anchor="nw", padx=24, pady=(24, 8))

        subtitle = tk.Label(
            self,
            text="Accédez à vos ressources d'étude enregistrées.",
            font=("Segoe UI", 12),
            bg=bg,
            fg=theme.WORKSPACE_MUTED,
        )
        subtitle.pack(anchor="nw", padx=24)
