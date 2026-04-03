"""Composants communs pour la barre latérale de navigation."""

import tkinter as tk


class Sidebar(tk.Frame):
    """Barre latérale avec boutons de navigation et état actif."""

    def __init__(self, master, on_select, 
                 bg: str = "#141429", 
                 active_fg: str = "#1DE9B6",
                 inactive_fg: str = "white",
                 **kwargs,
    ):
        super().__init__(master, bg=bg, **kwargs)
        
        self.on_select = on_select
        self.active_fg = active_fg
        self.inactive_fg = inactive_fg
        self._buttons = {}

        # Largeur fixe de la sidebar
        self.configure(width=250)
        self.grid_propagate(False)
        self.grid_columnconfigure(0, weight=1)

    # ---------- CONFIGURATION DES ENTRÉES DE MENU ----------

    def set_items(self, items: dict) -> None:
        """Crée les boutons de navigation à partir d'un dict {view_name: label}."""
        # Nettoyer les anciens widgets si on reconfigure le menu
        for child in self.winfo_children():
            child.destroy()
        self._buttons.clear()

        for index, (view_name, label) in enumerate(items.items()):
            btn = tk.Button(
                self,
                text=label,
                bg=self["bg"],
                fg=self.inactive_fg,
                activebackground=self["bg"],
                activeforeground=self.active_fg,
                bd=0,
                anchor="w",
                padx=20,
                pady=10,
                cursor="hand2",
                highlightthickness=0,
            )
            btn.grid(row=index, column=0, sticky="ew", pady=(10 if index == 0 else 5, 0))
            btn.configure(command=lambda vn=view_name: self._on_click(vn))
            self.grid_rowconfigure(index, weight=0)

            self._buttons[view_name] = btn

    # ---------- GESTION DE L'ÉTAT ACTIF ----------

    def _on_click(self, view_name: str) -> None:
        """Callback interne lorsqu'un bouton est cliqué."""
        self.set_active(view_name)
        if callable(self.on_select):
            self.on_select(view_name)

    def set_active(self, view_name: str) -> None:
        """Met à jour la couleur du texte du bouton actif."""
        for name, btn in self._buttons.items():
            if name == view_name:
                btn.configure(fg=self.active_fg)
            else:
                btn.configure(fg=self.inactive_fg)
