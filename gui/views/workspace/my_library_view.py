"""Vue Bibliothèque personnelle après connexion."""

import tkinter as tk
from tkinter import messagebox

from gui.messages import show_error
from gui.messages import show_info
import gui.views.common.theme as theme


class MyLibraryView(tk.Frame):
    """Page Bibliothèque personnelle: résumés publiés et évaluations reçues."""

    def __init__(
        self, root, app_controller, bg: str = theme.WORKSPACE_BACKGROUND, **kwargs
    ):
        """Construit la vue Bibliothèque personnelle."""
        super().__init__(master=root, bg=bg, **kwargs)
        self.app_controller = app_controller
        self.bg = bg

        # -------- Header --------
        self._make_label(
            "Ma bibliothèque", ("Segoe UI", 20, "bold"), fg=theme.WORKSPACE_TEXT
        ).pack(anchor="nw", padx=24, pady=(24, 8))
        self._make_label(
            "Gérez vos résumés publiés et consultez vos évaluations.",
            ("Segoe UI", 12),
            fg=theme.WORKSPACE_MUTED,
        ).pack(anchor="nw", padx=24)

        # -------- Summary cards --------
        self.summary_frame = tk.Frame(self, bg=bg)
        self.summary_frame.pack(fill="x", padx=24, pady=(16, 8))

        # -------- Scrollable content --------
        content_container = tk.Frame(self, bg=bg)
        content_container.pack(fill="both", expand=True, padx=24, pady=(0, 16))

        self.canvas = tk.Canvas(content_container, bg=bg, highlightthickness=0)
        self.scrollbar = tk.Scrollbar(
            content_container, orient="vertical", command=self.canvas.yview
        )
        self.scroll_frame = tk.Frame(self.canvas, bg=bg)
        self.canvas_window = self.canvas.create_window(
            (0, 0), window=self.scroll_frame, anchor="nw"
        )

        self.scroll_frame.bind(
            "<Configure>",
            lambda _event: self.canvas.configure(scrollregion=self.canvas.bbox("all")),
        )
        self.canvas.bind(
            "<Configure>",
            lambda event: self.canvas.itemconfigure(
                self.canvas_window, width=event.width
            ),
        )
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

    # --------------------------------------------------------
    # Méthodes de construction communes
    # --------------------------------------------------------

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
        """Crée un tk.Label sur fond blanc."""
        return self._make_label(
            text, font, parent=parent, fg=fg, bg=theme.COLORS.white, **kwargs
        )

    def _make_panel_frame(self, parent, **kwargs):
        """Crée un panneau blanc réutilisable."""
        return tk.Frame(
            parent,
            bg=theme.COLORS.white,
            padx=14,
            pady=14,
            highlightbackground=theme.WORKSPACE_BORDER,
            highlightthickness=1,
            **kwargs,
        )

    def _make_section_header(self, parent, title: str, subtitle: str) -> None:
        """Affiche le titre et le sous-titre d'une section."""
        self._make_panel_label(parent, title, ("Segoe UI", 13, "bold")).pack(
            anchor="w"
        )
        self._make_panel_label(
            parent, subtitle, ("Segoe UI", 9), fg=theme.WORKSPACE_MUTED
        ).pack(anchor="w", pady=(2, 10))

    def _make_empty_label(self, parent, text: str) -> None:
        """Affiche un message d'état vide dans une section."""
        self._make_panel_label(
            parent,
            text,
            ("Segoe UI", 10),
            fg=theme.WORKSPACE_MUTED,
            wraplength=520,
            justify="left",
        ).pack(anchor="w", pady=(4, 0))

    def _make_badge(self, parent, text: str, fg=None, bg=None) -> tk.Label:
        """Crée un petit badge discret."""
        return tk.Label(
            parent,
            text=text,
            font=("Segoe UI", 9, "bold"),
            bg=bg or theme.WORKSPACE_BACKGROUND,
            fg=fg or theme.WORKSPACE_NEUTRAL_TEXT,
            padx=8,
            pady=3,
        )

    def _make_action_button(self, parent, text: str, kind: str, command):
        """Bouton d'action compact, aligne sur les cartes de la boutique."""
        colors = {
            "edit": (theme.WORKSPACE_BLUE_DARK, theme.WORKSPACE_BLUE_LIGHT),
            "delete": (theme.WORKSPACE_RED, theme.WORKSPACE_ORANGE),
            "save": (theme.WORKSPACE_GREEN_DARK, theme.WORKSPACE_GREEN),
        }
        bg, active_bg = colors[kind]
        return tk.Button(
            parent,
            text=text,
            font=("Segoe UI", 9, "bold"),
            bg=bg,
            fg=theme.COLORS.white,
            activebackground=active_bg,
            activeforeground=theme.COLORS.white,
            bd=0,
            padx=10,
            pady=5,
            cursor="hand2",
            command=command,
        )

    def _stars_for_rating(self, rating: float) -> str:
        """Convertit une note 0-5 en étoiles pleines/vides."""
        filled = max(0, min(5, int(round(rating))))
        return "★" * filled + "☆" * (5 - filled)

    def _format_rating(self, rating: float) -> str:
        """Formate une note moyenne pour l'affichage."""
        if rating <= 0:
            return "Aucune note"
        return f"{rating:.1f}/5"

    def _rating_color(self, rating: float) -> str:
        """Retourne la couleur associée à une note moyenne."""
        if rating <= 0:
            return theme.WORKSPACE_MUTED
        if rating > 3:
            return theme.WORKSPACE_GREEN
        if rating >= 2.5:
            return theme.WORKSPACE_ORANGE
        return theme.WORKSPACE_RED

    def _make_rating_row(
        self, parent, rating: float, bg: str, color=None
    ) -> tk.Frame:
        """Construit une ligne d'étoiles et de note chiffrée."""
        row = tk.Frame(parent, bg=bg)
        star_color = color or theme.WORKSPACE_ORANGE
        text_color = color or theme.WORKSPACE_MUTED
        tk.Label(
            row,
            text=self._stars_for_rating(rating),
            font=("Segoe UI", 11, "bold"),
            bg=bg,
            fg=star_color,
        ).pack(side="left")
        tk.Label(
            row,
            text=self._format_rating(rating),
            font=("Segoe UI", 9, "bold"),
            bg=bg,
            fg=text_color,
        ).pack(side="left", padx=(8, 0))
        return row

    def _average_summary_rating(self, summaries) -> float:
        """Calcule la moyenne des notes des résumés qui ont reçu une évaluation."""
        rated = [
            summary.average_rating
            for summary in summaries
            if summary.average_rating
        ]
        if not rated:
            return 0
        return sum(rated) / len(rated)

    # --------------------------------------------------------
    # Méthodes de données et rendu
    # --------------------------------------------------------

    def refresh(self) -> None:
        """Recharge les résumés et évaluations de la bibliothèque."""
        data = self.app_controller.get_my_library_data()
        self._render_summary_cards(data.summaries, data.evaluations)
        self._render_content(data.summaries, data.evaluations)

    def _render_summary_cards(self, summaries, evaluations) -> None:
        """Affiche les indicateurs rapides en haut de page."""
        for child in self.summary_frame.winfo_children():
            child.destroy()

        average = self._average_summary_rating(summaries)
        cards = [
            ("Résumés publiés", str(len(summaries)), theme.COLORS.black),
            ("Note moyenne", self._format_rating(average), self._rating_color(average)),
            ("Évaluations reçues", str(len(evaluations)), theme.COLORS.gray_500),
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

    def _render_content(self, summaries, evaluations) -> None:
        """Reconstruit les sections de contenu."""
        for child in self.scroll_frame.winfo_children():
            child.destroy()

        self._build_summaries_section(summaries)
        self._build_evaluations_section(evaluations)

    # --------------------------------------------------------
    # Méthodes de construction des sections
    # --------------------------------------------------------

    def _build_summaries_section(self, summaries) -> None:
        """Construit la section listant les résumés publiés."""
        section = self._make_panel_frame(self.scroll_frame)
        section.pack(fill="x", pady=(0, 16))
        self._make_section_header(
            section,
            "Mes résumés publiés",
            "Retrouvez vos publications, leur cours et leur note moyenne.",
        )

        if not summaries:
            self._make_empty_label(
                section, "Aucun résumé publié pour le moment."
            )
            return

        cards_frame = tk.Frame(section, bg=theme.COLORS.white)
        cards_frame.pack(fill="x")
        for col in range(2):
            cards_frame.grid_columnconfigure(col, weight=1, uniform="summary_cards")

        for index, summary in enumerate(summaries):
            self._build_summary_card(
                cards_frame,
                summary,
                row=index // 2,
                column=index % 2,
            )

    def _build_evaluations_section(self, evaluations) -> None:
        """Construit la section listant les évaluations reçues."""
        section = self._make_panel_frame(self.scroll_frame)
        section.pack(fill="x", pady=(0, 4))
        self._make_section_header(
            section,
            "Évaluations reçues sur mes résumés",
            "Les derniers retours des autres étudiants, avec la note en un coup d'œil.",
        )

        if not evaluations:
            self._make_empty_label(
                section, "Aucune évaluation reçue pour l'instant."
            )
            return

        cards_frame = tk.Frame(section, bg=theme.COLORS.white)
        cards_frame.pack(fill="x")
        for col in range(2):
            cards_frame.grid_columnconfigure(col, weight=1, uniform="evaluation_cards")

        for index, evaluation in enumerate(evaluations):
            self._build_evaluation_card(
                cards_frame,
                evaluation,
                row=index // 2,
                column=index % 2,
            )

    # --------------------------------------------------------
    # Méthodes de construction des cartes
    # --------------------------------------------------------

    def _build_summary_card(self, parent, summary, row: int, column: int) -> None:
        """Construit une carte de résumé avec ses actions."""
        card = tk.Frame(
            parent,
            bg=theme.COLORS.white,
            padx=12,
            pady=12,
            highlightbackground=theme.WORKSPACE_BORDER,
            highlightthickness=1,
        )
        card.grid(row=row, column=column, sticky="nsew", padx=6, pady=6)

        header = tk.Frame(card, bg=theme.COLORS.white)
        header.pack(fill="x")
        self._make_panel_label(
            header,
            summary.title,
            ("Segoe UI", 12, "bold"),
            wraplength=380,
            justify="left",
        ).pack(side="left", fill="x", expand=True, anchor="w")
        self._make_badge(
            header,
            summary.course_code,
            fg=theme.COLORS.black,
        ).pack(side="right", padx=(10, 0))

        self._make_panel_label(
            card,
            summary.description or "Sans description.",
            ("Segoe UI", 10),
            fg=theme.WORKSPACE_MUTED,
            wraplength=500,
            justify="left",
            anchor="w",
        ).pack(fill="x", pady=(8, 10))

        self._make_panel_label(
            card,
            f"Publié le {summary.publication_date}",
            ("Segoe UI", 9),
            fg=theme.WORKSPACE_MUTED,
        ).pack(anchor="w", pady=(0, 8))

        self._make_rating_row(
            card,
            summary.average_rating,
            theme.COLORS.white,
        ).pack(anchor="w")

        footer = tk.Frame(card, bg=theme.COLORS.white)
        footer.pack(fill="x", pady=(12, 0))

        actions = tk.Frame(footer, bg=theme.COLORS.white)
        actions.pack(side="right")
        self._make_action_button(
            actions,
            "Modifier",
            "edit",
            lambda current=summary: self._edit_summary(current),
        ).pack(side="left", padx=(0, 8))
        self._make_action_button(
            actions,
            "Supprimer",
            "delete",
            lambda current=summary: self._delete_summary(current),
        ).pack(side="left")

    def _build_evaluation_card(
        self, parent, evaluation, row: int, column: int
    ) -> None:
        """Construit une carte d'évaluation reçue."""
        card = tk.Frame(
            parent,
            bg=theme.COLORS.white,
            padx=12,
            pady=12,
            highlightbackground=theme.WORKSPACE_BORDER,
            highlightthickness=1,
        )
        card.grid(row=row, column=column, sticky="nsew", padx=6, pady=6)

        header = tk.Frame(card, bg=theme.COLORS.white)
        header.pack(fill="x")
        self._make_panel_label(
            header,
            evaluation.summary_title,
            ("Segoe UI", 12, "bold"),
            wraplength=360,
            justify="left",
        ).pack(side="left", fill="x", expand=True, anchor="w")
        self._make_badge(
            header,
            f"Par {evaluation.evaluator_name}",
            fg=theme.WORKSPACE_GREEN_TEXT,
            bg=theme.WORKSPACE_GREEN_LIGHT,
        ).pack(side="right", padx=(10, 0))

        self._make_panel_label(
            card,
            evaluation.comment or "Sans commentaire.",
            ("Segoe UI", 10),
            fg=theme.WORKSPACE_MUTED,
            wraplength=500,
            justify="left",
            anchor="w",
        ).pack(fill="x", pady=(8, 10))

        self._make_rating_row(card, evaluation.rating, theme.COLORS.white).pack(
            anchor="w"
        )

    # --------------------------------------------------------
    # Méthodes d'actions
    # --------------------------------------------------------

    def _edit_summary(self, summary) -> None:
        """Action pour modifier le résumé via une fenêtre modale."""
        popup = tk.Toplevel(self)
        popup.title("Modifier le résumé")
        popup.geometry("520x390")
        popup.configure(bg=theme.WORKSPACE_BACKGROUND)
        popup.transient(self.winfo_toplevel())
        popup.grab_set()

        tk.Label(
            popup,
            text="Nouveau titre",
            bg=theme.WORKSPACE_BACKGROUND,
            fg=theme.WORKSPACE_TEXT,
            font=("Segoe UI", 10, "bold"),
        ).pack(anchor="w", padx=16, pady=(16, 4))

        title_entry = tk.Entry(popup, width=54)
        title_entry.insert(0, summary.title)
        title_entry.pack(fill="x", padx=16)

        tk.Label(
            popup,
            text="Description",
            bg=theme.WORKSPACE_BACKGROUND,
            fg=theme.WORKSPACE_TEXT,
            font=("Segoe UI", 10, "bold"),
        ).pack(anchor="w", padx=16, pady=(14, 4))

        content_text = tk.Text(popup, width=54, height=9)
        content_text.insert("1.0", summary.description or "")
        content_text.pack(fill="both", expand=True, padx=16)

        def save_changes() -> None:
            """Valide les modifications saisies dans la fenêtre modale."""
            new_title = title_entry.get().strip()
            new_content = content_text.get("1.0", tk.END).strip()

            result = self.app_controller.modify_summary(
                summary.summary_id, new_title, new_content
            )
            if result.success:
                popup.destroy()
                show_info(self, result.message)
            else:
                show_error(popup, result.message)

        self._make_action_button(
            popup,
            "Enregistrer",
            "save",
            save_changes,
        ).pack(anchor="e", padx=16, pady=16)

    def _delete_summary(self, summary) -> None:
        """Action déclenchée par le bouton Supprimer d'une carte."""
        confirm = messagebox.askyesno(
            "Attention",
            "Voulez-vous vraiment supprimer ce résumé de la base de données ?",
            parent=self,
        )
        if not confirm:
            return

        result = self.app_controller.remove_summary(summary.summary_id)
        if result.success:
            show_info(self, result.message)
        else:
            show_error(self, result.message)
