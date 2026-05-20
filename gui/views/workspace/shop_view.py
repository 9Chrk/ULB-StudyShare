"""Vue Shop post-login avec achat et activation d'objets cosmétiques."""

import tkinter as tk

from gui.messages import show_error
from gui.messages import show_info


class ShopView(tk.Frame):
    """Page boutique: catalogue, achat d'objets et activation des objets possédés."""

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
            ("Points", str(points), "#f59e0b"),
            ("Objets possédés", str(owned_count), "#10b981"),
        ]

        for label, value, color in cards:
            card = tk.Frame(self.summary_frame, bg="white", padx=16, pady=12)
            card.pack(side="left", padx=(0, 12))

            tk.Label(
                card,
                text=value,
                font=("Segoe UI", 18, "bold"),
                bg="white",
                fg=color,
            ).pack(anchor="w")
            tk.Label(
                card,
                text=label,
                font=("Segoe UI", 10),
                bg="white",
                fg="#6b7280",
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
                fg="#6b7280",
            ).pack(anchor="w", pady=8)
            return

        for item in catalogue:
            self._build_item_card(item, owned_ids)

    def _build_item_card(self, item, owned_ids) -> None:
        is_owned = item.item_id in owned_ids
        is_active = self._is_item_active(item.item_id, item.item_type)

        card = tk.Frame(self.scroll_frame, bg="white", padx=16, pady=12)
        card.pack(fill="x", pady=6)

        header = tk.Frame(card, bg="white")
        header.pack(fill="x")

        tk.Label(
            header,
            text=item.name,
            font=("Segoe UI", 12, "bold"),
            bg="white",
            fg="#111827",
        ).pack(side="left")

        tk.Label(
            header,
            text=item.item_type.upper(),
            font=("Segoe UI", 9, "bold"),
            bg="white",
            fg="#2563eb",
        ).pack(side="right")

        tk.Label(
            card,
            text=item.description,
            font=("Segoe UI", 10),
            bg="white",
            fg="#6b7280",
            wraplength=760,
            justify="left",
            anchor="w",
        ).pack(fill="x", pady=(6, 8))

        footer = tk.Frame(card, bg="white")
        footer.pack(fill="x")

        tk.Label(
            footer,
            text=f"{item.price_points} pts",
            font=("Segoe UI", 11, "bold"),
            bg="white",
            fg="#f59e0b",
        ).pack(side="left")

        status_text = "Possédé" if is_owned else "Disponible"
        status_color = "#10b981" if is_owned else "#6b7280"
        tk.Label(
            footer,
            text=status_text,
            font=("Segoe UI", 10, "bold"),
            bg="white",
            fg=status_color,
        ).pack(side="left", padx=14)

        actions = tk.Frame(footer, bg="white")
        actions.pack(side="right")

        if not is_owned:
            tk.Button(
                actions,
                text="Acheter",
                font=("Segoe UI", 10, "bold"),
                bg="#141429",
                fg="white",
                activebackground="#1B1B33",
                activeforeground="white",
                bd=0,
                padx=12,
                pady=6,
                cursor="hand2",
                command=lambda item_id=item.item_id: self._on_buy(item_id),
            ).pack(side="right")
            return

        if item.item_type in ("badge", "titre", "theme"):
            tk.Button(
                actions,
                text="Actif" if is_active else "Activer",
                font=("Segoe UI", 10, "bold"),
                bg="#10b981" if is_active else "#e5e7eb",
                fg="white" if is_active else "#111827",
                activebackground="#10b981" if is_active else "#d1d5db",
                activeforeground="white" if is_active else "#111827",
                bd=0,
                padx=12,
                pady=6,
                cursor="hand2",
                state="disabled" if is_active else "normal",
                command=lambda item_id=item.item_id: self._on_activate(item_id),
            ).pack(side="right")

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
