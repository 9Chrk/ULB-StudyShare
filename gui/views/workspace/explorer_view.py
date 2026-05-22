"""Vue Explorateur simple après connexion."""

import tkinter as tk

import gui.views.common.theme as theme


class ExplorerView(tk.Frame):
    """Page Explorateur simple pour la navigation latérale."""

    def __init__(
        self, root, app_controller, bg: str = theme.WORKSPACE_BACKGROUND, **kwargs
    ):
        """Construit la vue Explorateur affichée depuis la sidebar."""
        super().__init__(master=root, bg=bg, **kwargs)
        self.app_controller = app_controller

        title = tk.Label(
            self,
            text="Explorer",
            font=("Segoe UI", 20, "bold"),
            bg=bg,
            fg=theme.WORKSPACE_TEXT,
        )
        title.pack(anchor="nw", padx=24, pady=(24, 8))

        subtitle = tk.Label(
            self,
            text="Discover courses and new resources.",
            font=("Segoe UI", 12),
            bg=bg,
            fg=theme.WORKSPACE_MUTED,
        )
        subtitle.pack(anchor="nw", padx=24)
