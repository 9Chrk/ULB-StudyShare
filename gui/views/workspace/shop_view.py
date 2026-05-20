"""Vue Shop post-login avec achat et activation d'objets cosmétiques."""

import tkinter as tk

from gui.messages import show_error
from gui.messages import show_info


class ShopView(tk.Frame):
    """Page boutique: catalogue, achat d'objets et activation des objets possédés."""

    COLOR_BG = "#f3f4f6"
    COLOR_PANEL = "#ffffff"
    COLOR_TEXT = "#111827"
    COLOR_MUTED = "#6b7280"
    COLOR_BORDER = "#e5e7eb"
    COLOR_BLUE = "#3b82f6"
    COLOR_BLUE_DARK = "#2563eb"
    COLOR_GREEN = "#10b981"
    COLOR_GREEN_DARK = "#059669"
    COLOR_GREEN_SOFT = "#dcfce7"
    COLOR_GREEN_TEXT = "#166534"
    COLOR_NEUTRAL = "#f3f4f6"
    COLOR_NEUTRAL_TEXT = "#374151"
    COLOR_ORANGE = "#f59e0b"

    def __init__(self, root, app_controller, bg: str = "#f3f4f6", **kwargs):
        super().__init__(master=root, bg=bg, **kwargs)
        self.app_controller = app_controller
        self.bg = bg
        self.data = {}

        # Header
        tk.Label(
            self,
            text="Shop",
            font=("Segoe UI", 20, "bold"),
            bg=bg,
            fg="#111827",
        ).pack(anchor="nw", padx=24, pady=(24, 8))

        tk.Label(
            self,
            text="Achetez et activez vos objets cosmétiques.",
            font=("Segoe UI", 12),
            bg=bg,
            fg="#6b7280",
        ).pack(anchor="nw", padx=24)

        self.summary_frame = tk.Frame(self, bg=bg)
        self.summary_frame.pack(fill="x", padx=24, pady=(16, 8))

        content_container = tk.Frame(self, bg=bg)
        content_container.pack(fill="both", expand=True, padx=24, pady=(0, 16))

        self.canvas = tk.Canvas(content_container, bg=bg, highlightthickness=0)
        self.scrollbar = tk.Scrollbar(content_container, orient="vertical", command=self.canvas.yview)
        self.scroll_frame = tk.Frame(self.canvas, bg=bg)

        self.scroll_frame.bind(
            "<Configure>",
            lambda _event: self.canvas.configure(scrollregion=self.canvas.bbox("all")),
        )

        self.canvas.create_window((0, 0), window=self.scroll_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        self.reload_data()

    def reload_data(self) -> None:
        """Recharge les données shop et reconstruit l'affichage."""
        self.data = self.app_controller.get_shop_data()
        self._render_summary()
        self._render_catalogue()

    def _render_summary(self) -> None:
        for child in self.summary_frame.winfo_children():
            child.destroy()

        points = self.data.get("points", 0)
        owned_count = len(self.data.get("owned", []))

        cards = [
            ("Points", str(points), self.COLOR_GREEN),
            ("Objets possédés", str(owned_count), self.COLOR_BLUE),
        ]

        for label, value, color in cards:
            card = tk.Frame(
                self.summary_frame,
                bg=self.COLOR_PANEL,
                padx=16,
                pady=12,
                highlightbackground=self.COLOR_BORDER,
                highlightthickness=1,
            )
            card.pack(side="left", padx=(0, 12))

            tk.Label(
                card,
                text=value,
                font=("Segoe UI", 18, "bold"),
                bg=self.COLOR_PANEL,
                fg=color,
            ).pack(anchor="w")
            tk.Label(
                card,
                text=label,
                font=("Segoe UI", 10),
                bg=self.COLOR_PANEL,
                fg=self.COLOR_MUTED,
            ).pack(anchor="w")

    def _render_catalogue(self) -> None:
        for child in self.scroll_frame.winfo_children():
            child.destroy()

        catalogue = self.data.get("catalogue", [])
        owned_ids = set(self.data.get("owned", []))

        if not catalogue:
            tk.Label(
                self.scroll_frame,
                text="Aucun objet disponible pour le moment.",
                font=("Segoe UI", 11),
                bg=self.bg,
                fg=self.COLOR_MUTED,
            ).pack(anchor="w", pady=8)
            return

        sections = self._group_items_by_type(catalogue)

        top_frame = tk.Frame(self.scroll_frame, bg=self.bg)
        top_frame.pack(fill="x", expand=False)
        top_frame.grid_columnconfigure(0, weight=1)
        top_frame.grid_columnconfigure(1, weight=1)
        top_frame.grid_columnconfigure(2, weight=1)

        for index, item_type in enumerate(("badge", "titre", "theme")):
            section = self._build_section(top_frame, item_type, sections.get(item_type, []), owned_ids)
            section.grid(row=0, column=index, sticky="nsew", padx=(0 if index == 0 else 8, 0 if index == 2 else 8), pady=(0, 16))

        self._build_horizontal_section(self.scroll_frame, "autre", sections.get("autre", []), owned_ids)

    def _group_items_by_type(self, catalogue):
        sections = {"badge": [], "titre": [], "theme": [], "autre": []}
        for item in catalogue:
            if item.item_type in sections:
                sections[item.item_type].append(item)
            else:
                sections["autre"].append(item)
        return sections

    def _build_section(self, parent, item_type: str, items, owned_ids):
        section = tk.Frame(
            parent,
            bg=self.COLOR_PANEL,
            padx=14,
            pady=14,
            highlightbackground=self.COLOR_BORDER,
            highlightthickness=1,
        )

        title, accent, subtitle = self._section_meta(item_type)
        tk.Label(
            section,
            text=title,
            font=("Segoe UI", 13, "bold"),
            bg=self.COLOR_PANEL,
            fg=self.COLOR_TEXT,
        ).pack(anchor="w")

        tk.Label(
            section,
            text=subtitle,
            font=("Segoe UI", 9),
            bg=self.COLOR_PANEL,
            fg=self.COLOR_MUTED,
        ).pack(anchor="w", pady=(2, 10))

        items_frame = tk.Frame(section, bg=self.COLOR_PANEL)
        items_frame.pack(fill="both", expand=True)

        if not items:
            tk.Label(
                items_frame,
                text="Aucun objet dans cette catégorie.",
                font=("Segoe UI", 10),
                bg=self.COLOR_PANEL,
                fg=self.COLOR_MUTED,
                justify="left",
                wraplength=300,
            ).pack(anchor="w")
            return section

        for item in items:
            self._build_item_card(
                items_frame,
                item,
                owned_ids,
                accent_color=accent,
                vertical=True,
                wraplength=300,
            )

        return section

    def _build_horizontal_section(self, parent, item_type: str, items, owned_ids) -> None:
        section = tk.Frame(
            parent,
            bg=self.COLOR_PANEL,
            padx=14,
            pady=14,
            highlightbackground=self.COLOR_BORDER,
            highlightthickness=1,
        )
        section.pack(fill="x", pady=(0, 4))

        title, accent, subtitle = self._section_meta(item_type)
        tk.Label(
            section,
            text=title,
            font=("Segoe UI", 13, "bold"),
            bg=self.COLOR_PANEL,
            fg=self.COLOR_TEXT,
        ).pack(anchor="w")

        tk.Label(
            section,
            text=subtitle,
            font=("Segoe UI", 9),
            bg=self.COLOR_PANEL,
            fg=self.COLOR_MUTED,
        ).pack(anchor="w", pady=(2, 10))

        items_frame = tk.Frame(section, bg=self.COLOR_PANEL)
        items_frame.pack(fill="x")

        if not items:
            tk.Label(
                items_frame,
                text="Aucun objet dans cette catégorie.",
                font=("Segoe UI", 10),
                bg=self.COLOR_PANEL,
                fg=self.COLOR_MUTED,
            ).pack(anchor="w")
            return

        for item in items:
            self._build_item_card(
                items_frame,
                item,
                owned_ids,
                accent_color=accent,
                vertical=False,
                wraplength=220,
            )

    def _section_meta(self, item_type: str):
        if item_type == "badge":
            return "Badges", self.COLOR_GREEN, "Récompenses visuelles actives ou à acheter."
        if item_type == "titre":
            return "Titres", self.COLOR_BLUE, "Titres de profil à débloquer et activer."
        if item_type == "theme":
            return "Thèmes", self.COLOR_ORANGE, "Styles visuels du profil à équiper."
        return "Autres objets", self.COLOR_NEUTRAL_TEXT, "Objets disponibles mais sans activation spéciale."

    def _build_item_card(self, parent, item, owned_ids, accent_color: str, vertical: bool, wraplength: int) -> None:
        is_owned = item.item_id in owned_ids
        is_active = self._is_item_active(item.item_id, item.item_type)

        card = tk.Frame(
            parent,
            bg=self.COLOR_PANEL,
            padx=12,
            pady=12,
            highlightbackground=self.COLOR_BORDER,
            highlightthickness=1,
        )
        if vertical:
            card.pack(fill="x", pady=6)
        else:
            card.pack(side="left", fill="y", expand=True, padx=(0, 10), pady=6)

        header = tk.Frame(card, bg=self.COLOR_PANEL)
        header.pack(fill="x")

        tk.Label(
            header,
            text=item.name,
            font=("Segoe UI", 12, "bold"),
            bg=self.COLOR_PANEL,
            fg=self.COLOR_TEXT,
        ).pack(side="left")

        tk.Label(
            header,
            text=item.item_type.upper(),
            font=("Segoe UI", 9, "bold"),
            bg=self.COLOR_PANEL,
            fg=accent_color,
        ).pack(side="right")

        tk.Label(
            card,
            text=item.description,
            font=("Segoe UI", 10),
            bg=self.COLOR_PANEL,
            fg=self.COLOR_MUTED,
            wraplength=wraplength,
            justify="left",
            anchor="w",
        ).pack(fill="x", pady=(6, 8))

        footer = tk.Frame(card, bg=self.COLOR_PANEL)
        footer.pack(fill="x")

        tk.Label(
            footer,
            text=f"{item.price_points} pts",
            font=("Segoe UI", 11, "bold"),
            bg=self.COLOR_PANEL,
            fg=self.COLOR_GREEN,
        ).pack(side="left")

        status_text = "Possédé" if is_owned else "Disponible"
        status_color = self.COLOR_GREEN if is_owned else self.COLOR_MUTED
        status_bg = self.COLOR_GREEN_SOFT if is_owned else self.COLOR_NEUTRAL
        tk.Label(
            footer,
            text=status_text,
            font=("Segoe UI", 9, "bold"),
            bg=status_bg,
            fg=status_color,
            padx=8,
            pady=3,
        ).pack(side="left", padx=12)

        actions = tk.Frame(footer, bg=self.COLOR_PANEL)
        actions.pack(side="right")

        if not is_owned:
            self._make_action_button(
                actions,
                text="Acheter",
                kind="buy",
                command=lambda item_id=item.item_id: self._on_buy(item_id),
            ).pack(side="right")
            return

        if item.item_type in ("badge", "titre", "theme"):
            if is_active:
                tk.Label(
                    actions,
                    text="Activé",
                    font=("Segoe UI", 10, "bold"),
                    bg=self.COLOR_GREEN_SOFT,
                    fg=self.COLOR_GREEN_TEXT,
                    padx=12,
                    pady=6,
                ).pack(side="right")
            else:
                self._make_action_button(
                    actions,
                    text="Activer",
                    kind="activate",
                    command=lambda item_id=item.item_id: self._on_activate(item_id),
                ).pack(side="right")
            return

        tk.Label(
            actions,
            text="Aucune action",
            font=("Segoe UI", 10, "bold"),
            bg=self.COLOR_NEUTRAL,
            fg=self.COLOR_NEUTRAL_TEXT,
            padx=12,
            pady=6,
        ).pack(side="right")

    def _make_action_button(self, parent, text: str, kind: str, command):
        if kind == "buy":
            bg = self.COLOR_BLUE_DARK
            active_bg = self.COLOR_BLUE
        else:
            bg = self.COLOR_GREEN_DARK
            active_bg = self.COLOR_GREEN

        return tk.Button(
            parent,
            text=text,
            font=("Segoe UI", 10, "bold"),
            bg=bg,
            fg="white",
            activebackground=active_bg,
            activeforeground="white",
            bd=0,
            padx=12,
            pady=6,
            cursor="hand2",
            command=command,
        )

    def _is_item_active(self, item_id: int, item_type: str) -> bool:
        if item_type == "badge":
            return self.data.get("active_badge_id") == item_id
        if item_type == "titre":
            return self.data.get("active_title_id") == item_id
        if item_type == "theme":
            return self.data.get("active_theme_id") == item_id
        return False

    def _on_buy(self, item_id: int) -> None:
        result = self.app_controller.buy_shop_item(item_id)
        if result.get("success"):
            show_info(self, result.get("message", "Achat effectué."))
            self.reload_data()
            return
        show_error(self, result.get("message", "Achat impossible."))

    def _on_activate(self, item_id: int) -> None:
        result = self.app_controller.activate_shop_item(item_id)
        if result.get("success"):
            show_info(self, result.get("message", "Activation effectuée."))
            self.reload_data()
            return
        show_error(self, result.get("message", "Activation impossible."))
