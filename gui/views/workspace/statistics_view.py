"""Vue des statistiques globales de l'application."""

import tkinter as tk
from tkinter import ttk

import gui.views.common.theme as theme


def _format_float(value) -> str:
    """Formate un nombre avec deux décimales, ou '-' si absent."""
    if value is None:
        return "-"
    return f"{float(value):.2f}"


class StatisticsView(tk.Frame):
    """Affiche les huit statistiques demandées par le guide."""

    def __init__(
        self, root, app_controller, bg: str = theme.WORKSPACE_BACKGROUND, **kwargs
    ):
        """Construit la vue des statistiques globales et charge ses données."""
        super().__init__(master=root, bg=bg, **kwargs)
        self.app_controller = app_controller
        self.bg = bg

        # -------- Header --------
        tk.Label(
            self,
            text="Statistiques",
            font=("Segoe UI", 20, "bold"),
            bg=bg,
            fg=theme.WORKSPACE_TEXT,
        ).pack(anchor="nw", padx=24, pady=(24, 8))

        tk.Label(
            self,
            text="Vue d'ensemble des requêtes SQL demandées par l'énoncé.",
            font=("Segoe UI", 12),
            bg=bg,
            fg=theme.WORKSPACE_MUTED,
        ).pack(anchor="nw", padx=24)

        self.content_frame = tk.Frame(self, bg=bg)
        self.content_frame.pack(fill="both", expand=True)

    def refresh(self) -> None:
        """Recharge toutes les statistiques affichées."""
        data = self.app_controller.get_statistics_data()

        for child in self.content_frame.winfo_children():
            child.destroy()

        # -------- Summary cards --------
        self._build_summary_cards(data)

        # -------- Detailed tables --------
        self._build_scroll_area(data)

    def _build_summary_cards(self, data) -> None:
        """Construit les cartes de synthèse des statistiques globales."""
        # -------- Summary cards --------
        cards_frame = tk.Frame(self.content_frame, bg=self.bg)
        cards_frame.pack(fill="x", padx=24, pady=(16, 12))

        cards = [
            (
                "Moyenne résumés / utilisateur",
                _format_float(data.average_resumes_per_user),
                theme.WORKSPACE_GREEN,
            ),
            (
                "Objets cosmétiques top",
                self._format_top_object(data),
                theme.WORKSPACE_BLUE_LIGHT,
            ),
            (
                "Utilisateurs sans résumé",
                str(len(data.users_without_resumes)),
                theme.WORKSPACE_ORANGE,
            ),
            (
                "Utilisateurs en dépassement",
                str(len(data.overspending_users)),
                theme.WORKSPACE_BLUE_DARK,
            ),
        ]

        for index, (label, value, color) in enumerate(cards):
            card = tk.Frame(
                cards_frame,
                bg=theme.COLORS.white,
                padx=16,
                pady=12,
                highlightbackground=theme.WORKSPACE_BORDER,
                highlightthickness=1,
            )
            card.grid(
                row=0, column=index, sticky="nsew", padx=(0 if index == 0 else 10, 0)
            )
            cards_frame.grid_columnconfigure(index, weight=1)

            tk.Label(
                card,
                text=value,
                font=("Segoe UI", 18, "bold"),
                bg=theme.COLORS.white,
                fg=color,
            ).pack(anchor="w")
            tk.Label(
                card,
                text=label,
                font=("Segoe UI", 10),
                bg=theme.COLORS.white,
                fg=theme.WORKSPACE_MUTED,
            ).pack(anchor="w")

    def _build_scroll_area(self, data) -> None:
        """Construit la zone scrollable contenant les tableaux détaillés."""
        # -------- Tables container --------
        container = tk.Frame(self.content_frame, bg=self.bg)
        container.pack(fill="both", expand=True, padx=24, pady=(0, 16))

        self.canvas = tk.Canvas(container, bg=self.bg, highlightthickness=0)
        self.scrollbar = tk.Scrollbar(
            container, orient="vertical", command=self.canvas.yview
        )
        self.scroll_frame = tk.Frame(self.canvas, bg=self.bg)

        self.scroll_frame.bind(
            "<Configure>",
            lambda _event: self.canvas.configure(scrollregion=self.canvas.bbox("all")),
        )

        self.canvas.create_window((0, 0), window=self.scroll_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        self._build_sections(data)

    def _build_sections(self, data) -> None:
        """Déclare et construit toutes les sections statistiques."""
        # -------- Section registry --------
        # Chaque bloc relie un titre, une source de données et un renderer dédié.
        sections = [
            (
                "Top 10 utilisateurs",
                data.top_users,
                ("Rang", "Utilisateur", "Points", "Niveau"),
                self._rows_top_users,
            ),
            (
                "Utilisateurs avec au moins 3 cours distincts",
                data.multi_course_users,
                ("Utilisateur", "Cours", "Résumés"),
                self._rows_multi_course_users,
            ),
            (
                "Cours avec le plus de résumés",
                data.top_courses,
                ("Code", "Cours", "Crédits", "Résumés"),
                self._rows_top_courses,
            ),
            (
                "Meilleurs résumés par cours",
                data.best_rated_resumes,
                ("Code", "Cours", "Crédits", "Résumé", "Note moyenne"),
                self._rows_best_rated_resumes,
            ),
            (
                "Utilisateurs n'ayant jamais publié de résumé",
                data.users_without_resumes,
                ("Utilisateur", "E-mail", "Points"),
                self._rows_users_without_resumes,
            ),
            (
                "Utilisateurs ayant dépensé trop de points",
                data.overspending_users,
                ("Utilisateur", "Points", "Dépense", "Excédent"),
                self._rows_overspending_users,
            ),
        ]

        for title, rows, headers, row_builder in sections:
            self._build_table_section(title, rows, headers, row_builder)

    def _build_table_section(self, title: str, rows, headers, row_builder) -> None:
        """Construit une section tableau générique."""
        # -------- Table section --------
        section = tk.Frame(
            self.scroll_frame,
            bg=theme.COLORS.white,
            padx=14,
            pady=14,
            highlightbackground=theme.WORKSPACE_BORDER,
            highlightthickness=1,
        )
        section.pack(fill="x", pady=(0, 12))

        tk.Label(
            section,
            text=title,
            font=("Segoe UI", 13, "bold"),
            bg=theme.COLORS.white,
            fg=theme.WORKSPACE_TEXT,
        ).pack(anchor="w")

        table_frame = tk.Frame(section, bg=theme.COLORS.white)
        table_frame.pack(fill="x", pady=(10, 0))

        if not rows:
            # Les sections vides restent lisibles sans Treeview superflu.
            tk.Label(
                table_frame,
                text="Aucune donnée disponible.",
                font=("Segoe UI", 10),
                bg=theme.COLORS.white,
                fg=theme.WORKSPACE_MUTED,
            ).pack(anchor="w")
            return

        columns = tuple(f"c{i}" for i in range(len(headers)))
        tree = ttk.Treeview(
            table_frame, columns=columns, show="headings", height=min(len(rows), 8) or 1
        )
        for column_id, header in zip(columns, headers):
            tree.heading(column_id, text=header)
            tree.column(column_id, anchor="w", width=150, stretch=True)

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)

        row_builder(tree, rows)

        tree.pack(side="left", fill="x", expand=True)
        scrollbar.pack(side="right", fill="y")

    def _rows_top_users(self, tree, rows) -> None:
        """Insère les lignes de la statistique Top 10 utilisateurs."""
        # Les numéros de rang sont reconstruits à l'affichage.
        for index, row in enumerate(rows, start=1):
            tree.insert("", "end", values=(index, row.username, row.points, row.level))

    def _rows_multi_course_users(self, tree, rows) -> None:
        """Insère les utilisateurs ayant publié dans au moins trois cours."""
        for row in rows:
            tree.insert(
                "", "end", values=(row.username, row.course_count, row.resume_count)
            )

    def _rows_top_courses(self, tree, rows) -> None:
        """Insère les cours classés par nombre de résumés."""
        for row in rows:
            tree.insert(
                "", "end", values=(row.code, row.name, row.credits, row.resume_count)
            )

    def _rows_best_rated_resumes(self, tree, rows) -> None:
        """Insère les meilleurs résumés par cours."""
        for row in rows:
            tree.insert(
                "",
                "end",
                values=(
                    row.course_code,
                    row.course_name,
                    row.course_credits,
                    row.resume_title,
                    _format_float(row.average_rating),
                ),
            )

    def _rows_users_without_resumes(self, tree, rows) -> None:
        """Insère les utilisateurs qui n'ont jamais publié."""
        for row in rows:
            tree.insert("", "end", values=(row.username, row.email, row.points))

    def _rows_overspending_users(self, tree, rows) -> None:
        """Insère les utilisateurs dont les dépenses dépassent le solde."""
        for row in rows:
            tree.insert(
                "",
                "end",
                values=(row.username, row.points, row.total_spent, row.excess_spent),
            )

    def _format_top_object(self, data) -> str:
        """Retourne le libellé de l'objet cosmétique le plus acheté."""
        rows = data.most_bought_cosmetics
        if not rows:
            return "-"
        top_object = rows[0]
        return f"{top_object.name} ({top_object.purchase_count})"
