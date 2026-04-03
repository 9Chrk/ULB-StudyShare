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
        # Callbacks et styles
        self.on_select = on_select
        self.active_fg = active_fg
        self.inactive_fg = inactive_fg
        
        # Data des boutons
        self.buttons = {}
        self.exit_btn = None
        self.exit_row = 0
        
        # Largeur fixe de la sidebar
        self.configure(bg=bg, width=250)
        self.grid_propagate(False)              # Empêche la sidebar de se redimensionner selon son contenu
        self.grid_columnconfigure(0, weight=1)  # Permet aux boutons de s'étirer horizontalement
        
        # Style
        self.active_background = "#1B1B33"
        self.exit_btn_color = "#5B100F"


    # ---------- CONFIGURATION DES ENTRÉES DE MENU ----------

    def set_items(self, items: dict) -> None:
        """Crée les boutons de navigation à partir d'un dict {view_name: label}."""
        # Nettoyer les anciens widgets si on reconfigure le menu (sauf exit_btn)
        for child in self.winfo_children():
            if child != self.exit_btn:
                child.destroy()
        self.buttons.clear()

        for index, (view_name, label) in enumerate(items.items()):
            btn = tk.Button(
                self,
                text=label,
                font=("Segoe UI", 11, "bold"),
                bg=self["bg"],
                fg=self.inactive_fg,
                activebackground=self.active_background,
                activeforeground=self.active_fg,
                bd=0,
                anchor="w",
                padx=30,
                pady=10,
                cursor="hand2",
                highlightthickness=0,
            )
            btn.grid(row=index, column=0, sticky="ew", pady=(85 if index == 0 else 5, 0))
            btn.configure(command=lambda vn=view_name: self._on_click(vn))
            self.grid_rowconfigure(index, weight=0)

            self.buttons[view_name] = btn
        
        # Mémoriser la dernière ligne utilisée pour placer le bouton Exit en bas
        self.exit_row = len(items)


    # ---------- BOUTON EXIT ----------
    
    def add_exit_button(self, on_exit_callback) -> None:
        """Ajoute un bouton Exit en bas de la sidebar."""
       
        # Utiliser une ligne flexible pour pousser Exit en bas de la sidebar
        spacer_row = self.exit_row
        self.grid_rowconfigure(spacer_row, weight=1)

        # Séparateur visuel (ligne grise)
        separator = tk.Frame(self, bg="#333", height=1)
        separator.grid(row=spacer_row + 1, column=0, sticky="ew", pady=(20, 10), padx=20)
        
        # Bouton Exit
        self.exit_btn = tk.Button(
            self,
            text="Exit",
            font=("Segoe UI", 11, "bold"),
            bg=self["bg"],
            fg="white",
            activebackground=self.active_background,
            activeforeground="red",
            bd=0,
            anchor="w",
            padx=30,
            pady=10,
            cursor="hand2",
            highlightthickness=0,
            command=on_exit_callback,
        )
        self.exit_btn.grid(row=spacer_row + 2, column=0, sticky="ew", pady=(0, 16))
        self.grid_rowconfigure(spacer_row + 1, weight=0)
        self.grid_rowconfigure(spacer_row + 2, weight=0)


    # ---------- GESTION DE L'ÉTAT ACTIF ----------

    def _on_click(self, view_name: str) -> None:
        """Callback interne lorsqu'un bouton est cliqué."""
        self.set_active(view_name)
        if callable(self.on_select):
            self.on_select(view_name)

    def set_active(self, view_name: str) -> None:
        """Met à jour la couleur du texte du bouton actif."""
        for name, btn in self.buttons.items():
            if name == view_name:
                btn.configure(fg=self.active_fg, bg=self.active_background)
            else:
                btn.configure(fg=self.inactive_fg, bg=self["bg"])
