"""Vue Bibliotheque personnelle apres connexion."""

import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

from gui.messages import show_error
from gui.messages import show_info
import gui.views.common.theme as theme


class MyLibraryView(tk.Frame):
    """Page Bibliotheque personnelle: resumes publies et evaluations recues."""

    def __init__(
        self, root, app_controller, bg: str = theme.WORKSPACE_BACKGROUND, **kwargs
    ):
        """Construit la vue Bibliotheque personnelle."""
        super().__init__(master=root, bg=bg, **kwargs)
        self.app_controller = app_controller
        self.bg = bg
        self.summary_tree = None
        self.evaluation_tree = None
        self.summaries_by_id = {}

        # -------- Header --------
        tk.Label(
            self,
            text="Ma bibliothèque",
            font=("Segoe UI", 20, "bold"),
            bg=bg,
            fg=theme.WORKSPACE_TEXT,
        ).pack(anchor="nw", padx=24, pady=(24, 8))

        tk.Label(
            self,
            text="Gérez vos résumés publiés et consultez vos évaluations.",
            font=("Segoe UI", 12),
            bg=bg,
            fg=theme.WORKSPACE_MUTED,
        ).pack(anchor="nw", padx=24)

        self.content_frame = tk.Frame(self, bg=bg)
        self.content_frame.pack(fill="both", expand=True, padx=24, pady=(16, 16))

        self.refresh()

    def refresh(self) -> None:
        """Recharge les resumes et evaluations de la bibliotheque."""
        data = self.app_controller.get_my_library_data()

        for child in self.content_frame.winfo_children():
            child.destroy()

        self.summaries_by_id = {
            summary.summary_id: summary for summary in data.summaries
        }
        self._build_summaries_section(data.summaries)
        self._build_action_buttons()
        self._build_evaluations_section(data.evaluations)

    # ---------- BUILDERS ----------

    def _make_panel(self) -> tk.Frame:
        """Cree un panneau blanc reutilisable."""
        return tk.Frame(
            self.content_frame,
            bg=theme.COLORS.white,
            padx=14,
            pady=14,
            highlightbackground=theme.WORKSPACE_BORDER,
            highlightthickness=1,
        )

    def _make_panel_title(self, parent, text: str) -> None:
        tk.Label(
            parent,
            text=text,
            font=("Segoe UI", 13, "bold"),
            bg=theme.COLORS.white,
            fg=theme.WORKSPACE_TEXT,
        ).pack(anchor="w")

    def _build_summaries_section(self, summaries) -> None:
        section = self._make_panel()
        section.pack(fill="both", expand=True, pady=(0, 10))
        self._make_panel_title(section, "Mes résumés publiés")

        table_frame = tk.Frame(section, bg=theme.COLORS.white)
        table_frame.pack(fill="both", expand=True, pady=(10, 0))

        columns = ("id", "title", "course", "date", "rating")
        self.summary_tree = ttk.Treeview(
            table_frame, columns=columns, show="headings", selectmode="browse"
        )
        self.summary_tree.heading("id", text="ID")
        self.summary_tree.heading("title", text="Titre")
        self.summary_tree.heading("course", text="Cours")
        self.summary_tree.heading("date", text="Publication")
        self.summary_tree.heading("rating", text="Note moyenne")

        self.summary_tree.column("id", width=0, stretch=tk.NO)
        self.summary_tree.column("title", width=300, anchor="w")
        self.summary_tree.column("course", width=120, anchor="center")
        self.summary_tree.column("date", width=120, anchor="center")
        self.summary_tree.column("rating", width=120, anchor="center")

        scrollbar = ttk.Scrollbar(
            table_frame, orient="vertical", command=self.summary_tree.yview
        )
        self.summary_tree.configure(yscrollcommand=scrollbar.set)

        for summary in summaries:
            self.summary_tree.insert(
                "",
                tk.END,
                values=(
                    summary.summary_id,
                    summary.title,
                    summary.course_code,
                    str(summary.publication_date),
                    f"{summary.average_rating:.1f} / 5",
                ),
            )

        self.summary_tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def _build_action_buttons(self) -> None:
        actions = tk.Frame(self.content_frame, bg=self.bg)
        actions.pack(anchor="e", pady=(0, 14))

        tk.Button(
            actions,
            text="Modifier",
            font=("Segoe UI", 9, "bold"),
            bg=theme.WORKSPACE_BLUE_DARK,
            fg=theme.COLORS.white,
            activebackground=theme.WORKSPACE_BLUE_LIGHT,
            activeforeground=theme.COLORS.white,
            bd=0,
            padx=12,
            pady=6,
            cursor="hand2",
            command=self.edit_selected,
        ).pack(side="left", padx=(0, 8))

        tk.Button(
            actions,
            text="Supprimer",
            font=("Segoe UI", 9, "bold"),
            bg=theme.WORKSPACE_RED,
            fg=theme.COLORS.white,
            activebackground=theme.WORKSPACE_ORANGE,
            activeforeground=theme.COLORS.white,
            bd=0,
            padx=12,
            pady=6,
            cursor="hand2",
            command=self.delete_selected,
        ).pack(side="left")

    def _build_evaluations_section(self, evaluations) -> None:
        section = self._make_panel()
        section.pack(fill="both", expand=True)
        self._make_panel_title(section, "Évaluations reçues sur mes résumés")

        table_frame = tk.Frame(section, bg=theme.COLORS.white)
        table_frame.pack(fill="both", expand=True, pady=(10, 0))

        columns = ("title", "rating", "comment", "author")
        self.evaluation_tree = ttk.Treeview(
            table_frame, columns=columns, show="headings", selectmode="none"
        )
        self.evaluation_tree.heading("title", text="Résumé évalué")
        self.evaluation_tree.heading("rating", text="Note")
        self.evaluation_tree.heading("comment", text="Commentaire")
        self.evaluation_tree.heading("author", text="Par")

        self.evaluation_tree.column("title", width=220, anchor="w")
        self.evaluation_tree.column("rating", width=70, anchor="center")
        self.evaluation_tree.column("comment", width=360, anchor="w")
        self.evaluation_tree.column("author", width=130, anchor="center")

        scrollbar = ttk.Scrollbar(
            table_frame, orient="vertical", command=self.evaluation_tree.yview
        )
        self.evaluation_tree.configure(yscrollcommand=scrollbar.set)

        for evaluation in evaluations:
            self.evaluation_tree.insert(
                "",
                tk.END,
                values=(
                    evaluation.summary_title,
                    f"{evaluation.rating} / 5",
                    evaluation.comment or "-",
                    evaluation.evaluator_name,
                ),
            )

        self.evaluation_tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    # ---------- ACTIONS ----------

    def _get_selected_summary(self, action_label: str):
        selected_item = self.summary_tree.selection()
        if not selected_item:
            messagebox.showwarning(
                "Sélection requise",
                f"Sélectionnez le résumé à {action_label}.",
                parent=self,
            )
            return None

        values = self.summary_tree.item(selected_item[0], "values")
        summary_id = int(values[0])
        return self.summaries_by_id.get(summary_id)

    def edit_selected(self) -> None:
        """Action pour modifier le resume selectionne via une fenetre modale."""
        summary = self._get_selected_summary("modifier")
        if summary is None:
            return

        popup = tk.Toplevel(self)
        popup.title("Modifier le résumé")
        popup.geometry("460x360")
        popup.configure(bg=theme.WORKSPACE_BACKGROUND)
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
        content_text.insert("1.0", summary.description)
        content_text.pack(fill="both", expand=True, padx=16)

        def save_changes() -> None:
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

        tk.Button(
            popup,
            text="Enregistrer",
            font=("Segoe UI", 9, "bold"),
            bg=theme.WORKSPACE_GREEN_DARK,
            fg=theme.COLORS.white,
            activebackground=theme.WORKSPACE_GREEN,
            activeforeground=theme.COLORS.white,
            bd=0,
            padx=12,
            pady=6,
            cursor="hand2",
            command=save_changes,
        ).pack(anchor="e", padx=16, pady=16)

    def delete_selected(self) -> None:
        """Action declenchee par le bouton Supprimer."""
        summary = self._get_selected_summary("supprimer")
        if summary is None:
            return

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
