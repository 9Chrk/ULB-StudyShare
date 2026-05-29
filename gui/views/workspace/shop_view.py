"""Vue Boutique post-login avec achat et activation d'objets cosmétiques."""

import tkinter as tk

from gui.messages import show_error
from gui.messages import show_info
import gui.views.common.theme as theme


class ShopView(tk.Frame):
    """Page boutique: catalogue, achat d'objets et activation des objets possédés."""

    SECTION_META = {
        "badge": (
            "Badges",
            theme.WORKSPACE_GREEN,
            "Récompenses visuelles actives ou à acheter.",
        ),
        "titre": (
            "Titres",
            theme.WORKSPACE_BLUE_DARK,
            "Titres de profil à débloquer et activer.",
        ),
        "theme": (
            "Thèmes",
            theme.WORKSPACE_ORANGE,
            "Styles visuels du profil à équiper.",
        ),
        "autre": (
            "Autres objets",
            theme.WORKSPACE_NEUTRAL_TEXT,
            "Objets disponibles mais sans activation spéciale.",
        ),
    }

    def __init__(
        self, root, app_controller, bg: str = theme.WORKSPACE_BACKGROUND, **kwargs
    ):
        """Construit la vue Boutique et initialise ses zones de catalogue."""
        super().__init__(master=root, bg=bg, **kwargs)
        self.app_controller = app_controller
        self.bg = bg

        # -------- Header --------
        self._make_label(
            "Boutique", ("Segoe UI", 20, "bold"), fg=theme.WORKSPACE_TEXT
        ).pack(anchor="nw", padx=24, pady=(24, 8))
        self._make_label(
            "Achetez et activez vos objets cosmétiques.",
            ("Segoe UI", 12),
            fg=theme.WORKSPACE_MUTED,
        ).pack(anchor="nw", padx=24)

        # -------- Summary --------
        self.summary_frame = tk.Frame(self, bg=bg)
        self.summary_frame.pack(fill="x", padx=24, pady=(16, 8))

        # -------- Catalogue container --------
        content_container = tk.Frame(self, bg=bg)
        content_container.pack(fill="both", expand=True, padx=24, pady=(0, 16))

        self.canvas = tk.Canvas(content_container, bg=bg, highlightthickness=0)
        self.scrollbar = tk.Scrollbar(
            content_container, orient="vertical", command=self.canvas.yview
        )
        self.scroll_frame = tk.Frame(self.canvas, bg=bg)

        self.scroll_frame.bind(
            "<Configure>",
            lambda _event: self.canvas.configure(scrollregion=self.canvas.bbox("all")),
        )

        self.canvas.create_window((0, 0), window=self.scroll_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

    # ── helpers ────────────────────────────────────────────────────────────

    def _make_label(self, text, font, parent=None, fg=None, bg=None, **kwargs):
        """Crée un tk.Label avec les valeurs par défaut de la vue."""
        return tk.Label(
            parent or self,
            text=text,
            font=font,
            bg=bg or self.bg,
            fg=fg or theme.WORKSPACE_TEXT,
            **kwargs,
        )

    def _make_panel_label(self, parent, text, font, fg=None, **kwargs):
        """Crée un tk.Label sur fond COLOR_PANEL."""
        return self._make_label(
            text, font, parent=parent, fg=fg, bg=theme.COLORS.white, **kwargs
        )

    def _make_panel_frame(self, parent, **kwargs):
        """Crée un Frame avec le style carte (fond blanc + bordure)."""
        return tk.Frame(
            parent,
            bg=theme.COLORS.white,
            padx=14,
            pady=14,
            highlightbackground=theme.WORKSPACE_BORDER,
            highlightthickness=1,
            **kwargs,
        )

    def _make_section_header(self, parent, item_type: str) -> None:
        """Affiche le titre et le sous-titre d'une section."""
        title, _, subtitle = self.SECTION_META[item_type]
        self._make_panel_label(parent, title, ("Segoe UI", 13, "bold")).pack(anchor="w")
        self._make_panel_label(
            parent, subtitle, ("Segoe UI", 9), fg=theme.WORKSPACE_MUTED
        ).pack(anchor="w", pady=(2, 10))

    def _make_empty_label(self, parent) -> None:
        self._make_panel_label(
            parent,
            "None objet dans cette catégorie.",
            ("Segoe UI", 10),
            fg=theme.WORKSPACE_MUTED,
        ).pack(anchor="w")

    # ── data & render ──────────────────────────────────────────────────────

    def refresh(self) -> None:
        """Recharge les données shop et reconstruit l'affichage."""
        data = self.app_controller.get_shop_data()
        self._render_summary(data)
        self._render_catalogue(data)

    def _render_summary(self, data) -> None:
        # -------- Summary cards --------
        for child in self.summary_frame.winfo_children():
            child.destroy()

        cards = [
            ("Points", str(data.points), theme.COLORS.black),
            ("Objets possédés", str(len(data.owned)), theme.COLORS.gray_500),
        ]

        for label, value, color in cards:
            card = tk.Frame(
                self.summary_frame,
                bg=theme.COLORS.white,
                padx=16,
                pady=12,
                highlightbackground=theme.WORKSPACE_BORDER,
                highlightthickness=1,
            )
            card.pack(side="left", padx=(0, 12))
            self._make_panel_label(
                card, value, ("Segoe UI", 18, "bold"), fg=color
            ).pack(anchor="w")
            self._make_panel_label(
                card, label, ("Segoe UI", 10), fg=theme.WORKSPACE_MUTED
            ).pack(anchor="w")

    def _render_catalogue(self, data) -> None:
        # -------- Catalogue --------
        for child in self.scroll_frame.winfo_children():
            child.destroy()

        catalogue = data.catalogue
        owned_ids = set(data.owned)

        if not catalogue:
            # État vide: on évite de construire des sections inutiles.
            self._make_label(
                "None objet disponible pour le moment.",
                ("Segoe UI", 11),
                fg=theme.WORKSPACE_MUTED,
            ).pack(anchor="w", pady=8)
            return

        sections = self._group_items_by_type(catalogue)

        top_frame = tk.Frame(self.scroll_frame, bg=self.bg)
        top_frame.pack(fill="x", pady=(0, 16))
        for col in range(3):
            top_frame.grid_columnconfigure(col, weight=1)

        for index, item_type in enumerate(("badge", "titre", "theme")):
            section = self._build_section(
                top_frame, item_type, sections.get(item_type, []), owned_ids, data
            )
            padx = (0 if index == 0 else 8, 0 if index == 2 else 8)
            section.grid(row=0, column=index, sticky="nsew", padx=padx)

        self._build_horizontal_section(
            self.scroll_frame, "autre", sections.get("autre", []), owned_ids, data
        )

    def _group_items_by_type(self, catalogue):
        # On sépare le catalogue par type pour choisir ensuite le bon gabarit.
        sections = {"badge": [], "titre": [], "theme": [], "autre": []}
        for item in catalogue:
            sections[item.item_type if item.item_type in sections else "autre"].append(
                item
            )
        return sections

    # ── section builders ───────────────────────────────────────────────────

    def _build_section(self, parent, item_type: str, items, owned_ids, data):
        """Section verticale (badge, titre, theme)."""
        # -------- Vertical section --------
        _, accent, _ = self.SECTION_META[item_type]
        section = self._make_panel_frame(parent)
        self._make_section_header(section, item_type)

        items_frame = tk.Frame(section, bg=theme.COLORS.white)
        items_frame.pack(fill="both", expand=True)

        if not items:
            self._make_empty_label(items_frame)
        else:
            for item in items:
                self._build_item_card(
                    items_frame,
                    item,
                    owned_ids,
                    data,
                    accent_color=accent,
                    vertical=True,
                    wraplength=300,
                )

        return section

    def _build_horizontal_section(
        self, parent, item_type: str, items, owned_ids, data
    ) -> None:
        """Section horizontale (autre)."""
        # -------- Horizontal section --------
        _, accent, _ = self.SECTION_META[item_type]
        section = self._make_panel_frame(parent)
        section.pack(fill="x", pady=(0, 4))
        self._make_section_header(section, item_type)

        if item_type == "autre":
            items_frame = tk.Frame(section, bg=theme.COLORS.white)
            items_frame.pack(fill="x")
            for col in range(3):
                items_frame.grid_columnconfigure(col, weight=1)
        else:
            scroller = self._create_horizontal_scroller(section, height=190)
            scroller["container"].pack(fill="x")
            items_frame = scroller["inner"]

        if not items:
            self._make_empty_label(items_frame)
            return

        if item_type == "autre":
            for index, item in enumerate(items):
                self._build_item_card(
                    items_frame,
                    item,
                    owned_ids,
                    data,
                    accent_color=accent,
                    vertical=True,
                    wraplength=220,
                    layout="grid",
                    row=index // 3,
                    column=index % 3,
                )
        else:
            for item in items:
                self._build_item_card(
                    items_frame,
                    item,
                    owned_ids,
                    data,
                    accent_color=accent,
                    vertical=False,
                    wraplength=220,
                )

    def _create_horizontal_scroller(self, parent, height: int):
        container = tk.Frame(parent, bg=self.bg)
        canvas = tk.Canvas(container, bg=self.bg, height=height, highlightthickness=0)
        scrollbar = tk.Scrollbar(container, orient="horizontal", command=canvas.xview)
        inner = tk.Frame(canvas, bg=self.bg)

        canvas.create_window((0, 0), window=inner, anchor="nw")
        inner.bind(
            "<Configure>", lambda _: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        canvas.configure(xscrollcommand=scrollbar.set)
        canvas.pack(side="top", fill="both", expand=True)
        scrollbar.pack(side="bottom", fill="x")

        return {
            "container": container,
            "canvas": canvas,
            "inner": inner,
            "scrollbar": scrollbar,
        }

    # ── item card ──────────────────────────────────────────────────────────

    def _build_item_card(
        self,
        parent,
        item,
        owned_ids,
        data,
        accent_color: str,
        vertical: bool,
        wraplength: int,
        layout: str = "pack",
        row: int = 0,
        column: int = 0,
    ) -> None:
        # -------- Item card --------
        is_owned = item.item_id in owned_ids
        is_active = self._is_item_active(item.item_id, item.item_type, data)

        card = tk.Frame(
            parent,
            bg=theme.COLORS.white,
            padx=12,
            pady=12,
            highlightbackground=theme.WORKSPACE_BORDER,
            highlightthickness=1,
        )
        if layout == "grid":
            card.grid(row=row, column=column, sticky="nsew", padx=6, pady=6)
        elif vertical:
            card.pack(fill="x", pady=6)
        else:
            card.configure(width=250)
            card.pack(side="left", fill="y", padx=(0, 10), pady=6)

        self._make_panel_label(card, item.name, ("Segoe UI", 12, "bold")).pack(
            anchor="w"
        )
        self._make_panel_label(
            card,
            item.description,
            ("Segoe UI", 10),
            fg=theme.WORKSPACE_MUTED,
            wraplength=wraplength,
            justify="left",
            anchor="w",
        ).pack(fill="x", pady=(6, 8))

        footer = tk.Frame(card, bg=theme.COLORS.white)
        footer.pack(fill="x")

        self._make_panel_label(
            footer,
            f"{item.price_points} pts",
            ("Segoe UI", 10, "bold"),
            fg=theme.WORKSPACE_GREEN,
        ).pack(side="left")

        status_text = "Possédé" if is_owned else "Disponible"
        status_fg = theme.WORKSPACE_GREEN if is_owned else theme.WORKSPACE_MUTED
        status_bg = (
            theme.WORKSPACE_GREEN_LIGHT if is_owned else theme.WORKSPACE_BACKGROUND
        )
        # Le badge d'état résume immédiatement si l'objet peut encore être acheté.
        tk.Label(
            footer,
            text=status_text,
            font=("Segoe UI", 9, "bold"),
            bg=status_bg,
            fg=status_fg,
            padx=8,
            pady=3,
        ).pack(side="left", padx=12)

        actions = tk.Frame(footer, bg=theme.COLORS.white)
        actions.pack(side="right")

        if not is_owned:
            # Les objets non possédés n'exposent qu'une action d'achat.
            self._make_action_button(
                actions,
                "Acheter",
                "buy",
                lambda iid=item.item_id: self._on_action("buy", iid),
            ).pack(side="right")
        elif item.item_type in ("badge", "titre", "theme"):
            if is_active:
                # Un objet cosmétique actif est seulement signalé comme tel.
                tk.Label(
                    actions,
                    text="Activé",
                    font=("Segoe UI", 9, "bold"),
                    bg=status_bg,
                    fg=status_fg,
                    padx=8,
                    pady=3,
                ).pack(side="right")
            else:
                self._make_action_button(
                    actions,
                    "Activer",
                    "activate",
                    lambda iid=item.item_id: self._on_action("activate", iid),
                ).pack(side="right")
        else:
            # Les objets sans mécanique d'activation restent informatifs.
            tk.Label(
                actions,
                text="Nonee action",
                font=("Segoe UI", 10, "bold"),
                bg=theme.WORKSPACE_BACKGROUND,
                fg=theme.WORKSPACE_NEUTRAL_TEXT,
                padx=12,
                pady=6,
            ).pack(side="right")

    def _make_action_button(self, parent, text: str, kind: str, command):
        bg, active_bg = (
            (theme.WORKSPACE_BLUE_DARK, theme.WORKSPACE_BLUE_LIGHT)
            if kind == "buy"
            else (theme.WORKSPACE_GREEN_DARK, theme.WORKSPACE_GREEN)
        )
        return tk.Button(
            parent,
            text=text,
            font=("Segoe UI", 9, "bold"),
            bg=bg,
            fg=theme.COLORS.white,
            activebackground=active_bg,
            activeforeground=theme.COLORS.white,
            bd=0,
            width=9,
            padx=10,
            pady=5,
            cursor="hand2",
            command=command,
        )

    # ── Aide à l'état ──────────────────────────────────────────────────────

    def _is_item_active(self, item_id: int, item_type: str, data) -> bool:
        # Chaque type cosmétique a une seule clé d'état actif dans BoutiqueData.
        key = {
            "badge": "active_badge_id",
            "titre": "active_title_id",
            "theme": "active_theme_id",
        }.get(item_type)
        return key is not None and getattr(data, key) == item_id

    def _on_action(self, kind: str, item_id: int) -> None:
        """Gère achat et activation via un unique handler."""
        # -------- Actions --------
        if kind == "buy":
            result = self.app_controller.buy_shop_item(item_id)
            default_ok, default_err = "Achat effectué.", "Achat impossible."
        else:
            result = self.app_controller.activate_shop_item(item_id)
            default_ok, default_err = "Activation effectuée.", "Activation impossible."

        if result.success:
            show_info(self, result.message or default_ok)
        else:
            show_error(self, result.message or default_err)
