"""Composants communs pour la barre latérale de navigation."""

import tkinter as tk

from gui.ui_helpers import get_asset_path


class Sidebar(tk.Frame):
    """Barre latérale avec boutons de navigation et état actif."""

    def __init__(self, master, on_select, 
                 bg: str = "#141429", 
                 active_fg: str = "#1DE9B6",
                 inactive_fg: str = "white",
                 **kwargs,
    ):
        super().__init__(master, bg=bg, **kwargs)
        
        # Data et callbacks
        self.buttons = {}
        self.icons = {}
        self.logo_image = None
        self.on_select = on_select
        
        # Offset pour les boutons de menu
        self.start_row = 2
        self.exit_row = 0
        
        # Largeur fixe de la sidebar
        self.configure(bg=bg, width=250)
        self.grid_propagate(False)              # Empêche la sidebar de se redimensionner selon son contenu
        self.grid_columnconfigure(0, weight=1)  # Permet aux boutons de s'étirer horizontalement
        
        # Style
        self.active_fg = active_fg
        self.inactive_fg = inactive_fg
        self.active_background = "#1B1B33"
        self.exit_btn_color = "#5B100F"

        # Header branding
        self.build_header()

    
    # --------- CONSTRUCTION DE L'EN-TÊTE DE MARQUE ----------

    def build_header(self) -> None:
        """Construit l'en-tête de marque en haut de la sidebar."""
        brand_frame = tk.Frame(self, bg=self["bg"])
        brand_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=(18, 14))

        # Logo ULB 
        try:
            self.logo_image = tk.PhotoImage(file=str(get_asset_path("assets", "images", "ulb_logo.png"))).subsample(12, 12)
            logo_label = tk.Label(brand_frame, image=self.logo_image, bg=self["bg"])
            logo_label.pack(side="left")
            
        # (fallback silencieux si l'asset n'est pas disponible) 
        except tk.TclError:
            pass
        
        # Titre de l'application à côté du logo
        title_label = tk.Label(brand_frame, text="StudyShare", font=("Segoe UI", 16, "bold"), bg=self["bg"], fg="white")
        title_label.pack(side="left", padx=(10, 0))
        
        # Séparateur visuel
        top_separator = tk.Frame(self, bg="#2A2A45", height=1)
        top_separator.grid(row=1, column=0, sticky="ew", padx=20, pady=(0, 10))


    # ---------- CONFIGURATION DES ENTRÉES DE MENU ----------

    def set_items(self, items: dict) -> None:
        """Crée les boutons de navigation à partir d'un dict {view_name: label}."""
        
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
            row = self.start_row + index
            btn.grid(row=row, column=0, sticky="ew", pady=(10 if index == 0 else 5, 0))
            btn.configure(command=lambda vn=view_name: self.on_click(vn))
            self.grid_rowconfigure(row, weight=0)
            
            # Mémoriser le bouton pour la gestion de l'état actif
            self.buttons[view_name] = btn
        
        # Mémoriser la dernière ligne utilisée pour placer le bouton Exit en bas
        self.exit_row = self.start_row + len(items)


    # ---------- BOUTON LOG OUT ----------
    
    def add_exit_button(self, on_exit_callback) -> None:
        """Ajoute un bouton Log out en bas de la sidebar."""
        
        # Utiliser une ligne flexible pour pousser Exit en bas de la sidebar
        self.grid_rowconfigure(self.exit_row, weight=1)

        # Séparateur visuel
        exit_separator = tk.Frame(self, bg="#333", height=1)
        exit_separator.grid(row=self.exit_row + 1, column=0, sticky="ew", pady=(20, 10), padx=20)
        
        # Bouton Log out
        exit_btn = tk.Button(
            self,
            text="Log out",
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
        exit_btn.grid(row=self.exit_row + 2, column=0, sticky="ew", pady=(0, 16))
        self.grid_rowconfigure(self.exit_row + 1, weight=0)
        self.grid_rowconfigure(self.exit_row + 2, weight=0)


    # ---------- GESTION DE L'ÉTAT ACTIF ----------

    def on_click(self, view_name: str) -> None:
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
