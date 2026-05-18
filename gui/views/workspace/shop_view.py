"""Simple post-login Shop view."""

import tkinter as tk


class ShopView(tk.Frame):
    """Simple Shop page for sidebar navigation."""

    def __init__(self, root, app_controller, bg: str = "#f3f4f6", **kwargs):
        super().__init__(master=root, bg=bg, **kwargs)
        self.app_controller = app_controller

        title = tk.Label(
            self,
            text="Shop",
            font=("Segoe UI", 20, "bold"),
            bg=bg,
            fg="#111827",
        )
        title.pack(anchor="nw", padx=24, pady=(24, 8))

        subtitle = tk.Label(
            self,
            text="Redeem rewards and unlock extras.",
            font=("Segoe UI", 12),
            bg=bg,
            fg="#6b7280",
        )
        subtitle.pack(anchor="nw", padx=24)

        data = self.app_controller.get_shop_data()
        catalogue = data.get("catalogue", [])
        owned = data.get("owned", [])

        canvas = tk.Canvas(self, bg=bg, highlightthickness=0)
        scrollbar = tk.Scrollbar(self, orient="vertical", command=canvas.yview)
        scroll_frame = tk.Frame(canvas, bg=bg)

        scroll_frame.bind("<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True, padx=24, pady=16)
        scrollbar.pack(side="right", fill="y")

        for id_obj, nom, desc, prix in catalogue:
            is_owned = id_obj in owned
            card = tk.Frame(scroll_frame, bg="white", padx=16, pady=12)
            card.pack(fill="x", pady=4)

            tk.Label(card, text=nom, font=("Segoe UI", 12, "bold"),
                     bg="white", fg="#111827").pack(anchor="w")

            tk.Label(card, text=desc, font=("Segoe UI", 10),
                     bg="white", fg="#6b7280", wraplength=600,
                     anchor="w").pack(fill="x")

            bottom = tk.Frame(card, bg="white")
            bottom.pack(fill="x", pady=(4, 0))

            tk.Label(bottom, text=f"{prix} pts",
                     font=("Segoe UI", 11, "bold"),
                     bg="white", fg="#f59e0b").pack(side="left")

            status = "✓ Owned" if is_owned else "Available"
            color = "#10b981" if is_owned else "#6b7280"
            tk.Label(bottom, text=status, font=("Segoe UI", 10),
                     bg="white", fg=color).pack(side="left", padx=16)
