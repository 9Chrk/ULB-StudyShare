"""Vue des statistiques globales de l'application."""

import tkinter as tk
from tkinter import ttk


class StatisticsView(tk.Frame):
    """Affiche les huit statistiques demandées par le guide."""

    COLOR_BG = "#f3f4f6"
    COLOR_PANEL = "#ffffff"
    COLOR_TEXT = "#111827"
    COLOR_MUTED = "#6b7280"
    COLOR_BORDER = "#e5e7eb"
    COLOR_BLUE = "#3b82f6"
    COLOR_BLUE_DARK = "#2563eb"
    COLOR_GREEN = "#10b981"
    COLOR_ORANGE = "#f59e0b"

    def __init__(self, root, app_controller, bg: str = "#f3f4f6", **kwargs):
        super().__init__(master=root, bg=bg, **kwargs)
        self.app_controller = app_controller
        self.bg = bg
        self.data = self.app_controller.get_statistics_data()

        tk.Label(
            self,
            text="Statistics",
            font=("Segoe UI", 20, "bold"),
            bg=bg,
            fg=self.COLOR_TEXT,
        ).pack(anchor="nw", padx=24, pady=(24, 8))

        tk.Label(
            self,
            text="Vue d'ensemble des indicateurs demandés par l'énoncé.",
            font=("Segoe UI", 12),
            bg=bg,
            fg=self.COLOR_MUTED,
        ).pack(anchor="nw", padx=24)

        self._build_summary_cards()
        self._build_scroll_area()

    def _build_summary_cards(self) -> None:
        cards_frame = tk.Frame(self, bg=self.bg)
        cards_frame.pack(fill="x", padx=24, pady=(16, 12))

        cards = [
            ("Moyenne resumes / utilisateur", self._format_float(self.data.get("average_resumes_per_user")), self.COLOR_GREEN),
            ("Objets cosmetiques top", self._format_top_object(), self.COLOR_BLUE),
            ("Utilisateurs sans resume", str(len(self.data.get("users_without_resumes", []))), self.COLOR_ORANGE),
            ("Utilisateurs en depassement", str(len(self.data.get("overspending_users", []))), self.COLOR_BLUE_DARK),
        ]

        for index, (label, value, color) in enumerate(cards):
            card = tk.Frame(
                cards_frame,
                bg=self.COLOR_PANEL,
                padx=16,
                pady=12,
                highlightbackground=self.COLOR_BORDER,
                highlightthickness=1,
            )
            card.grid(row=0, column=index, sticky="nsew", padx=(0 if index == 0 else 10, 0))
            cards_frame.grid_columnconfigure(index, weight=1)

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

    def _build_scroll_area(self) -> None:
        container = tk.Frame(self, bg=self.bg)
        container.pack(fill="both", expand=True, padx=24, pady=(0, 16))

        self.canvas = tk.Canvas(container, bg=self.bg, highlightthickness=0)
        self.scrollbar = tk.Scrollbar(container, orient="vertical", command=self.canvas.yview)
        self.scroll_frame = tk.Frame(self.canvas, bg=self.bg)

        self.scroll_frame.bind(
            "<Configure>",
            lambda _event: self.canvas.configure(scrollregion=self.canvas.bbox("all")),
        )

        self.canvas.create_window((0, 0), window=self.scroll_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        self._build_sections()

    def _build_sections(self) -> None:
        sections = [
            ("Top 10 utilisateurs", self.data.get("top_users", []), ("Rang", "Utilisateur", "Points", "Niveau"), self._rows_top_users),
            ("Utilisateurs avec au moins 3 cours distincts", self.data.get("multi_course_users", []), ("Utilisateur", "Cours", "Resumes"), self._rows_multi_course_users),
            ("Cours avec le plus de resumes", self.data.get("top_courses", []), ("Code", "Cours", "Resumes"), self._rows_top_courses),
            ("Meilleurs resumes par cours", self.data.get("best_rated_resumes", []), ("Code", "Cours", "Resume", "Note moyenne"), self._rows_best_rated_resumes),
            ("Utilisateurs n'ayant jamais publie", self.data.get("users_without_resumes", []), ("Utilisateur", "Email", "Points"), self._rows_users_without_resumes),
            ("Utilisateurs ayant depense trop de points", self.data.get("overspending_users", []), ("Utilisateur", "Points", "Depense", "Excedent"), self._rows_overspending_users),
        ]

        for title, rows, headers, row_builder in sections:
            self._build_table_section(title, rows, headers, row_builder)

    def _build_table_section(self, title: str, rows, headers, row_builder) -> None:
        section = tk.Frame(
            self.scroll_frame,
            bg=self.COLOR_PANEL,
            padx=14,
            pady=14,
            highlightbackground=self.COLOR_BORDER,
            highlightthickness=1,
        )
        section.pack(fill="x", pady=(0, 12))

        tk.Label(
            section,
            text=title,
            font=("Segoe UI", 13, "bold"),
            bg=self.COLOR_PANEL,
            fg=self.COLOR_TEXT,
        ).pack(anchor="w")

        table_frame = tk.Frame(section, bg=self.COLOR_PANEL)
        table_frame.pack(fill="x", pady=(10, 0))

        if not rows:
            tk.Label(
                table_frame,
                text="Aucune donnée disponible.",
                font=("Segoe UI", 10),
                bg=self.COLOR_PANEL,
                fg=self.COLOR_MUTED,
            ).pack(anchor="w")
            return

        columns = tuple(f"c{i}" for i in range(len(headers)))
        tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=min(len(rows), 8) or 1)
        for column_id, header in zip(columns, headers):
            tree.heading(column_id, text=header)
            tree.column(column_id, anchor="w", width=150, stretch=True)

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)

        row_builder(tree, rows)

        tree.pack(side="left", fill="x", expand=True)
        scrollbar.pack(side="right", fill="y")

    def _rows_top_users(self, tree, rows) -> None:
        for index, (username, points, level) in enumerate(rows, start=1):
            tree.insert("", "end", values=(index, username, points, level))

    def _rows_multi_course_users(self, tree, rows) -> None:
        for username, course_count, resume_count in rows:
            tree.insert("", "end", values=(username, course_count, resume_count))

    def _rows_top_courses(self, tree, rows) -> None:
        for code_cours, nom_cours, resume_count in rows:
            tree.insert("", "end", values=(code_cours, nom_cours, resume_count))

    def _rows_best_rated_resumes(self, tree, rows) -> None:
        for code_cours, nom_cours, titre, avg_note in rows:
            tree.insert("", "end", values=(code_cours, nom_cours, titre, self._format_float(avg_note)))

    def _rows_users_without_resumes(self, tree, rows) -> None:
        for username, email, points in rows:
            tree.insert("", "end", values=(username, email, points))

    def _rows_overspending_users(self, tree, rows) -> None:
        for username, points, total_spent, excess_spent in rows:
            tree.insert("", "end", values=(username, points, total_spent, excess_spent))

    def _format_float(self, value) -> str:
        if value is None:
            return "-"
        return f"{float(value):.2f}"

    def _format_top_object(self) -> str:
        rows = self.data.get("most_bought_cosmetics", [])
        if not rows:
            return "-"
        _, name, _, _, count = rows[0]
        return f"{name} ({count})"
