"""Composants communs pour la barre laterale de navigation."""

import tkinter as tk
from typing import Dict, Optional
from PIL import Image, ImageTk, ImageOps

from gui.ui_helpers import get_asset_path


class Sidebar(tk.Frame):
    """Barre laterale avec boutons de navigation et etat actif."""

    def __init__(self, master, on_select,
                 bg: str = "#141429",
                 active_fg: str = "#1DE9B6",
                 inactive_fg: str = "white",
                 **kwargs,
    ):
        super().__init__(master, bg=bg, **kwargs)

        # Data et callbacks
        self.buttons: Dict[str, tk.Button] = {}
        self.icons: Dict[str, Dict[str, Optional[tk.PhotoImage]]] = {}
        self.indicators: Dict[str, tk.Frame] = {}
        self.logout_icon: Optional[tk.PhotoImage] = None
        self.logo_image = None
        self.on_select = on_select

        # Offset pour les boutons de menu
        self.start_row = 2
        self.exit_row = 0

        # Largeur fixe de la sidebar
        self.configure(bg=bg, width=250)
        self.grid_propagate(False)
        
        # Colonne 0 = indicateur, colonne 1 = contenu
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)

        # Style
        self.active_fg = active_fg
        self.inactive_fg = inactive_fg
        self.active_background = "#1B1B33"
        self.exit_btn_color = "#5B100F"

        # Header branding
        self.build_header()


    # --------- CONSTRUCTION DE L'ENTETE DE MARQUE ----------

    def build_header(self) -> None:
        """Construit l'entete de marque en haut de la sidebar."""
        brand_frame = tk.Frame(self, bg=self["bg"])
        brand_frame.grid(row=0, column=0, columnspan=2, sticky="ew", padx=20, pady=(18, 14))

        # Logo ULB
        try:
            self.logo_image = (
                tk.PhotoImage(file=str(get_asset_path("assets", "images", "ulb_logo.png")))
                .subsample(12, 12)
            )
            logo_label = tk.Label(brand_frame, image=self.logo_image, bg=self["bg"])
            logo_label.pack(side="left")
        except tk.TclError:
            # fallback silencieux si l'asset n'est pas disponible
            pass

        # Titre de l'application
        title_label = tk.Label(
            brand_frame,
            text="StudyShare",
            font=("Segoe UI", 16, "bold"),
            bg=self["bg"],
            fg="white",
        )
        title_label.pack(side="left", padx=(10, 0))

        # Separateur visuel
        top_separator = tk.Frame(self, bg="#2A2A45", height=1)
        top_separator.grid(row=1, column=0, columnspan=2, sticky="ew", padx=20, pady=(0, 10))


    # ---------- CONFIGURATION DES ENTREES DE MENU ----------

    def set_items(self, items: Dict[str, str]) -> None:
        """Cree les boutons de navigation a partir d'un dict {view_name: label}."""
        for index, (view_name, label) in enumerate(items.items()):
            row = self.start_row + index
            pad_y = (10 if index == 0 else 5, 0)

            # Indicateur vertical a gauche du bouton
            indicator = tk.Frame(self, bg=self["bg"], width=3)
            indicator.grid(row=row, column=0, sticky="ns", pady=pad_y)

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
            # Placer le bouton dans la grille
            btn.grid(row=row, column=1, sticky="ew", pady=pad_y)
            btn.configure(command=lambda vn=view_name: self.on_click(vn))
            self.grid_rowconfigure(row, weight=0)

            self.buttons[view_name] = btn
            self.indicators[view_name] = indicator

        # Derniere ligne utilisee pour placer le bouton Log out en bas
        self.exit_row = self.start_row + len(items)


    # ---------- BOUTON LOG OUT ----------

    def add_exit_button(self, on_exit_callback) -> None:
        """Ajoute un bouton Log out en bas de la sidebar."""
        # Utiliser une ligne flexible pour pousser Log out en bas
        self.grid_rowconfigure(self.exit_row, weight=1)

        # Separateur visuel
        exit_separator = tk.Frame(self, bg="#333", height=1)
        exit_separator.grid(row=self.exit_row + 1, column=0, columnspan=2, sticky="ew", pady=(20, 10), padx=20)

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

        # Icone de logout
        icon = self.load_icon_for("logout", active=False)
        if icon is not None:
            self.logout_icon = icon
            exit_btn.configure(image=icon, compound="left", padx=16)

        # Placer le bouton Log out en bas de la sidebar
        exit_btn.grid(row=self.exit_row + 2, column=0, columnspan=2, sticky="ew", pady=(0, 16))
        self.grid_rowconfigure(self.exit_row + 1, weight=0)
        self.grid_rowconfigure(self.exit_row + 2, weight=0)
        

    # ---------- GESTION DE L'ETAT ACTIF ----------

    def on_click(self, view_name: str) -> None:
        """Callback interne lorsqu'un bouton est clique."""
        self.set_active(view_name)
        if callable(self.on_select):
            self.on_select(view_name)

    def set_active(self, view_name: str) -> None:
        """Met a jour la couleur du texte et les icones des boutons."""
        for name, btn in self.buttons.items():
            is_active = name == view_name
            indicator = self.indicators.get(name)

            # Indicateur vertical et couleur du texte selon l'etat actif/inactif
            if is_active:
                btn.configure(fg=self.active_fg, bg=self.active_background)
                if indicator is not None:
                    indicator.configure(bg=self.active_fg)
            else:
                btn.configure(fg=self.inactive_fg, bg=self["bg"])
                if indicator is not None:
                    indicator.configure(bg=self["bg"])

            # Charger les icones si necessaire
            icon_set = self.icons.get(name)
            if icon_set is None:
                icon_set = {
                    "inactive": self.load_icon_for(name, active=False),
                    "active": self.load_icon_for(name, color_active=self.active_fg, active=True),
                }
                self.icons[name] = icon_set

            # Choisir l'icone a afficher selon l'etat actif/inactif
            img = icon_set.get("active") if is_active and icon_set.get("active") is not None else icon_set.get("inactive")
            if img is not None:
                btn.configure(image=img, compound="left", padx=16)
            else:
                btn.configure(image="", padx=30)
                

    # ---------- ICONES DE MENU ----------

    def load_icon_for(self, view_name: str, color_active: str = None, active: bool = False):
        """Charge et teinte une icone pour une vue donnee.

        - utilise les fichiers fournis dans assets/images
        - applique une teinte verte pour l'etat actif (self.active_fg)
          et un gris neutre pour l'etat inactif
        """

        icon_map = {
            "dashboard": "home.ico",
            "my_library": "open-book.ico",
            "explorer": "loupe.ico",
            "statistics": "statistics.ico",
            "leaderboard": "podium.ico",
            "shop": "shopping-cart.ico",
            "profile": "user.ico",
            "logout": "logout.ico",
        }
        # Trouver le nom de fichier correspondant a la vue
        base_name = icon_map.get(view_name)
        if base_name is None:
            return None
        
        # Construire le chemin vers l'asset
        path = get_asset_path("assets", "images", base_name)
        
        try:
            img = Image.open(path).convert("RGBA")
        except Exception:
            return None

        img = img.resize((18, 18), Image.LANCZOS)

        # Couleur selon l'etat actif/inactif
        color = color_active if active else "#9CA3AF"
        
        # Charger l'image et appliquer la teinte
        gray = ImageOps.grayscale(img)
        colored = ImageOps.colorize(gray, black="#000000", white=color)
        alpha = img.split()[-1]
        colored.putalpha(alpha)

        return ImageTk.PhotoImage(colored)
