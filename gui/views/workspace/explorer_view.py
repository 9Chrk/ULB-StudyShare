"""Vue Explorateur: recherche de cours, publication et evaluation de resumes."""

import tkinter as tk
from tkinter import ttk

from gui.messages import show_error
from gui.messages import show_info
import gui.views.common.theme as theme


class ExplorerView(tk.Frame):
    """Page explorateur avec recherche de cours et resumes publics."""

    def __init__(
        self, root, app_controller, bg: str = theme.WORKSPACE_BACKGROUND, **kwargs
    ):
        """Construit la vue explorateur et charge les donnees initiales."""
        super().__init__(master=root, bg=bg, **kwargs)
        self.app_controller = app_controller
        self.bg = bg
        self.current_course_code = None
        self.academic_years = []
        self._rendering_courses = False

        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=2)
        self.grid_columnconfigure(1, weight=15)

        # -------- Header --------
        self._make_label(
            "Explorateur", ("Segoe UI", 20, "bold"), fg=theme.WORKSPACE_TEXT
        ).grid(row=0, column=0, columnspan=2, sticky="nw", padx=24, pady=(24, 8))
        self._make_label(
            "Recherchez un cours, publiez un resume et evaluez les contributions.",
            ("Segoe UI", 12),
            fg=theme.WORKSPACE_MUTED,
        ).grid(row=1, column=0, columnspan=2, sticky="nw", padx=24)

        self._build_course_panel()
        self._build_summary_panel()

        self.refresh()

    # ---------- HELPERS ----------

    def _make_label(self, text, font, parent=None, fg=None, bg=None, **kwargs):
        """Cree un tk.Label avec les valeurs par defaut de la vue."""
        return tk.Label(
            parent or self,
            text=text,
            font=font,
            bg=bg or self.bg,
            fg=fg or theme.WORKSPACE_TEXT,
            **kwargs,
        )

    def _make_panel_label(self, parent, text, font, fg=None, **kwargs):
        """Cree un tk.Label sur fond blanc."""
        return self._make_label(
            text, font, parent=parent, fg=fg, bg=theme.COLORS.white, **kwargs
        )

    def _make_panel_frame(self, parent, **kwargs):
        """Cree un panneau blanc réutilisable."""
        return tk.Frame(
            parent,
            bg=theme.COLORS.white,
            padx=14,
            pady=14,
            highlightbackground=theme.WORKSPACE_BORDER,
            highlightthickness=1,
            **kwargs,
        )

    def _make_action_button(self, parent, text: str, kind: str, command, **kwargs):
        """Bouton d'action compact."""
        colors = {
            "primary": (theme.WORKSPACE_BLUE_DARK, theme.WORKSPACE_BLUE_LIGHT),
            "success": (theme.WORKSPACE_GREEN_DARK, theme.WORKSPACE_GREEN),
            "neutral": (theme.COLORS.gray_500, theme.WORKSPACE_NEUTRAL_TEXT),
        }
        bg, active_bg = colors[kind]
        return tk.Button(
            parent,
            text=text,
            font=("Segoe UI", 9, "bold"),
            bg=bg,
            fg=theme.COLORS.white,
            disabledforeground=theme.COLORS.white,
            activebackground=active_bg,
            activeforeground=theme.COLORS.white,
            bd=0,
            padx=10,
            pady=5,
            cursor="hand2",
            command=command,
            **kwargs,
        )

    def _format_rating(self, rating: float, count: int) -> str:
        if count <= 0:
            return "Aucune note"
        return f"{rating:.1f}/5 ({count})"

    # ---------- LAYOUT ----------

    def _build_course_panel(self) -> None:
        panel = self._make_panel_frame(self)
        panel.grid(row=2, column=0, sticky="nsew", padx=(24, 8), pady=(16, 24))
        panel.grid_rowconfigure(2, weight=1)
        panel.grid_columnconfigure(0, weight=1)

        self._make_panel_label(panel, "Cours", ("Segoe UI", 13, "bold")).grid(
            row=0, column=0, sticky="w"
        )
        self._make_panel_label(
            panel,
            "Filtrez par code, nom ou faculté.",
            ("Segoe UI", 9),
            fg=theme.WORKSPACE_MUTED,
        ).grid(row=1, column=0, sticky="w", pady=(2, 10))

        search_frame = tk.Frame(panel, bg=theme.COLORS.white)
        search_frame.grid(row=2, column=0, sticky="nsew")
        search_frame.grid_rowconfigure(1, weight=1)
        search_frame.grid_columnconfigure(0, weight=1)

        actions = tk.Frame(search_frame, bg=theme.COLORS.white)
        actions.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        actions.grid_columnconfigure(0, weight=1)

        self.search_var = tk.StringVar()
        self.search_entry = tk.Entry(actions, textvariable=self.search_var)
        self.search_entry.grid(row=0, column=0, sticky="ew", padx=(0, 8))
        self.search_entry.bind("<Return>", lambda _event: self.refresh())

        self._make_action_button(
            actions, "Chercher", "primary", self.refresh, width=9
        ).grid(row=0, column=1, padx=(0, 8))
        self._make_action_button(
            actions, "Ajouter", "success", self.popup_add_course, width=9
        ).grid(row=0, column=2)

        columns = ("code", "name", "faculty")
        self.course_tree = ttk.Treeview(
            search_frame, columns=columns, show="headings", selectmode="browse"
        )
        self.course_tree.heading("code", text="Code")
        self.course_tree.heading("name", text="Cours")
        self.course_tree.heading("faculty", text="Faculté")
        self.course_tree.column("code", width=100, stretch=False)
        self.course_tree.column("name", width=220, stretch=True)
        self.course_tree.column("faculty", width=130, stretch=True)
        self.course_tree.grid(row=1, column=0, sticky="nsew")
        self.course_tree.bind("<<TreeviewSelect>>", self.on_course_select)

    def _build_summary_panel(self) -> None:
        panel = self._make_panel_frame(self)
        panel.grid(row=2, column=1, sticky="nsew", padx=(8, 24), pady=(16, 24))
        panel.grid_rowconfigure(2, weight=1)
        panel.grid_columnconfigure(0, weight=1)

        header = tk.Frame(panel, bg=theme.COLORS.white)
        header.grid(row=0, column=0, sticky="ew")
        header.grid_columnconfigure(0, weight=1)

        self.selected_course_label = self._make_panel_label(
            header, "Selectionnez un cours", ("Segoe UI", 13, "bold")
        )
        self.selected_course_label.grid(row=0, column=0, sticky="w")

        self.publish_button = self._make_action_button(
            header,
            "Publier",
            "primary",
            self.popup_publish,
            state="disabled",
            width=9,
        )
        self.publish_button.grid(row=0, column=1, sticky="e")

        self.summary_hint = self._make_panel_label(
            panel,
            "Les resumes publics du cours selectionne apparaitront ici.",
            ("Segoe UI", 9),
            fg=theme.WORKSPACE_MUTED,
        )
        self.summary_hint.grid(row=1, column=0, sticky="w", pady=(2, 10))

        columns = ("id", "title", "author", "date", "rating")
        self.summary_tree = ttk.Treeview(
            panel,
            columns=columns,
            displaycolumns=("title", "author", "date", "rating"),
            show="headings",
            selectmode="browse",
        )
        self.summary_tree.heading("id", text="ID")
        self.summary_tree.heading("title", text="Titre")
        self.summary_tree.heading("author", text="Auteur")
        self.summary_tree.heading("date", text="Date")
        self.summary_tree.heading("rating", text="Note")
        self.summary_tree.column("id", width=0, minwidth=0, stretch=False)
        self.summary_tree.column("title", width=250, stretch=True)
        self.summary_tree.column("author", width=140, stretch=True)
        self.summary_tree.column("date", width=95, stretch=False)
        self.summary_tree.column("rating", width=130, stretch=False)
        self.summary_tree.grid(row=2, column=0, sticky="nsew")

        footer = tk.Frame(panel, bg=theme.COLORS.white)
        footer.grid(row=3, column=0, sticky="ew", pady=(10, 0))
        self._make_action_button(
            footer, "Évaluer", "success", self.popup_evaluate, width=10
        ).pack(side="right")

    # ---------- DATA & RENDER ----------

    def refresh(self) -> None:
        """Recharge les cours et les resumes de la selection courante."""
        data = self.app_controller.get_explorer_data(
            self.search_var.get(), self.current_course_code or ""
        )
        self.academic_years = data.academic_years
        self._render_courses(data.courses)
        self._render_summaries(data.summaries if self.current_course_code else [])

    def _render_courses(self, courses) -> None:
        """Reconstruit la liste des cours."""
        selected_code = self.current_course_code
        self._rendering_courses = True
        for item in self.course_tree.get_children():
            self.course_tree.delete(item)

        try:
            course_codes = set()
            for course in courses:
                course_codes.add(course.code)
                self.course_tree.insert(
                    "",
                    "end",
                    iid=course.code,
                    values=(course.code, course.name, course.faculty),
                )

            if selected_code in course_codes:
                self.course_tree.selection_set(selected_code)
                self.course_tree.focus(selected_code)
            elif selected_code is not None:
                self.current_course_code = None
                self._update_selected_course_label()
        finally:
            self._rendering_courses = False

    def _render_summaries(self, summaries) -> None:
        """Reconstruit la liste des resumes du cours selectionne."""
        for item in self.summary_tree.get_children():
            self.summary_tree.delete(item)

        for summary in summaries:
            self.summary_tree.insert(
                "",
                "end",
                values=(
                    summary.summary_id,
                    summary.title,
                    summary.author,
                    summary.publication_date,
                    self._format_rating(
                        summary.average_rating, summary.evaluation_count
                    ),
                ),
            )

        self._update_selected_course_label()

    def _update_selected_course_label(self) -> None:
        if self.current_course_code:
            self.selected_course_label.config(
                text=f"Resumes pour {self.current_course_code}"
            )
            self.publish_button.config(state="normal")
        else:
            self.selected_course_label.config(text="Selectionnez un cours")
            self.publish_button.config(state="disabled")

    # ---------- EVENTS ----------

    def on_course_select(self, _event=None) -> None:
        """Charge les resumes quand un cours est selectionne."""
        if self._rendering_courses:
            return
        selection = self.course_tree.selection()
        if not selection:
            return
        selected_course_code = str(selection[0])
        if selected_course_code == self.current_course_code:
            return
        self.current_course_code = selected_course_code
        self.refresh()

    # ---------- ACTIONS ----------

    def popup_add_course(self) -> None:
        popup = tk.Toplevel(self)
        popup.title("Nouveau cours")
        popup.geometry("360x250")
        popup.configure(bg=theme.WORKSPACE_BACKGROUND)
        popup.transient(self.winfo_toplevel())
        popup.grab_set()

        code_entry = self._add_popup_entry(popup, "Code")
        name_entry = self._add_popup_entry(popup, "Nom")
        faculty_entry = self._add_popup_entry(popup, "Faculté")

        def save() -> None:
            result = self.app_controller.add_explorer_course(
                code_entry.get(), name_entry.get(), faculty_entry.get()
            )
            if result.success:
                popup.destroy()
                show_info(self, result.message)
            else:
                show_error(popup, result.message)

        self._make_action_button(popup, "Ajouter", "success", save).pack(
            anchor="e", padx=16, pady=16
        )

    def popup_publish(self) -> None:
        if not self.current_course_code:
            show_error(self, "Selectionnez un cours.")
            return

        popup = tk.Toplevel(self)
        popup.title("Publier un resume")
        popup.geometry("520x430")
        popup.configure(bg=theme.WORKSPACE_BACKGROUND)
        popup.transient(self.winfo_toplevel())
        popup.grab_set()

        self._make_label(
            f"Cours: {self.current_course_code}",
            ("Segoe UI", 11, "bold"),
            parent=popup,
            bg=theme.WORKSPACE_BACKGROUND,
            fg=theme.WORKSPACE_BLUE_DARK,
        ).pack(anchor="w", padx=16, pady=(16, 8))

        title_entry = self._add_popup_entry(popup, "Titre")

        self._make_label(
            "Année académique",
            ("Segoe UI", 10, "bold"),
            parent=popup,
            bg=theme.WORKSPACE_BACKGROUND,
        ).pack(anchor="w", padx=16, pady=(12, 4))
        year_combo = ttk.Combobox(
            popup, values=self.academic_years, state="readonly", width=46
        )
        if self.academic_years:
            year_combo.set(self.academic_years[0])
        year_combo.pack(fill="x", padx=16)

        self._make_label(
            "Description",
            ("Segoe UI", 10, "bold"),
            parent=popup,
            bg=theme.WORKSPACE_BACKGROUND,
        ).pack(anchor="w", padx=16, pady=(12, 4))
        content_text = tk.Text(popup, height=8)
        content_text.pack(fill="both", expand=True, padx=16)

        def save() -> None:
            result = self.app_controller.publish_summary(
                self.current_course_code,
                title_entry.get(),
                content_text.get("1.0", tk.END),
                year_combo.get(),
            )
            if result.success:
                popup.destroy()
                show_info(self, result.message)
            else:
                show_error(popup, result.message)

        self._make_action_button(popup, "Publier", "primary", save).pack(
            anchor="e", padx=16, pady=16
        )

    def popup_evaluate(self) -> None:
        selection = self.summary_tree.selection()
        if not selection:
            show_error(self, "Selectionnez un resume.")
            return

        summary_id = int(self.summary_tree.item(selection[0], "values")[0])
        popup = tk.Toplevel(self)
        popup.title("Évaluer")
        popup.geometry("360x260")
        popup.configure(bg=theme.WORKSPACE_BACKGROUND)
        popup.transient(self.winfo_toplevel())
        popup.grab_set()

        rating_entry = self._add_popup_entry(popup, "Note")
        comment_entry = self._add_popup_entry(popup, "Commentaire")

        def save() -> None:
            try:
                rating = int(rating_entry.get())
            except ValueError:
                show_error(popup, "Note invalide.")
                return

            result = self.app_controller.rate_summary(
                summary_id, rating, comment_entry.get()
            )
            if result.success:
                popup.destroy()
                show_info(self, result.message)
            else:
                show_error(popup, result.message)

        self._make_action_button(popup, "Envoyer", "success", save).pack(
            anchor="e", padx=16, pady=16
        )

    def _add_popup_entry(self, popup, label: str) -> tk.Entry:
        self._make_label(
            label,
            ("Segoe UI", 10, "bold"),
            parent=popup,
            bg=theme.WORKSPACE_BACKGROUND,
        ).pack(anchor="w", padx=16, pady=(12, 4))
        entry = tk.Entry(popup)
        entry.pack(fill="x", padx=16)
        return entry
