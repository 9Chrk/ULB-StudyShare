import tkinter as tk
from tkinter import ttk, messagebox

class MyLibraryView(tk.Frame):
    def __init__(self, master, app_controller, **kwargs):
        # pour éviter le crash
        bg_color = kwargs.pop('bg', 'white')
        super().__init__(master, **kwargs)
        self.app_controller = app_controller
        self.configure(bg=bg_color)
        
        self.columnconfigure(0, weight=1)
        self.rowconfigure(2, weight=1) # Espace pour les résumés
        self.rowconfigure(5, weight=1) # Espace pour les évaluations

        title_lbl = tk.Label(
            self, text="Ma bibliothèque", font=("Helvetica", 24, "bold"), bg=bg_color, fg="#111827"
        )
        title_lbl.grid(row=0, column=0, sticky="w", padx=20, pady=(20, 5))

        subtitle_lbl = tk.Label(
            self, text="Gérez vos résumés publiés et consultez vos évaluations.", 
            font=("Helvetica", 14), bg=bg_color, fg="#6B7280"
        )
        subtitle_lbl.grid(row=1, column=0, sticky="w", padx=20, pady=(0, 10))

        # partie : mes résumés 
        columns_res = ("id", "titre", "cours", "note")
        self.tree = ttk.Treeview(self, columns=columns_res, show="headings", selectmode="browse")
        
        self.tree.heading("id", text="ID")
        self.tree.heading("titre", text="Titre du résumé")
        self.tree.heading("cours", text="Cours")
        self.tree.heading("note", text="Note Moyenne")

        self.tree.column("id", width=0, stretch=tk.NO)
        self.tree.column("titre", width=300, anchor="w")
        self.tree.column("cours", width=150, anchor="center")
        self.tree.column("note", width=100, anchor="center")

        self.tree.grid(row=2, column=0, sticky="nsew", padx=20, pady=5)

        scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=2, column=1, sticky="ns", pady=5)

        # Boutons d'action pour les résumés
        btn_frame = tk.Frame(self, bg=bg_color)
        btn_frame.grid(row=3, column=0, sticky="e", padx=20, pady=5)

        self.edit_btn = tk.Button(btn_frame, text="Modifier", fg="blue", command=self.edit_selected)
        self.edit_btn.pack(side="left", padx=10)

        self.delete_btn = tk.Button(btn_frame, text="Supprimer", fg="red", command=self.delete_selected)
        self.delete_btn.pack(side="left")

        # la partie des evaluations
        eval_title = tk.Label(
            self, text="Évaluations reçues sur mes résumés", font=("Helvetica", 16, "bold"), bg=bg_color, fg="#111827"
        )
        eval_title.grid(row=4, column=0, sticky="w", padx=20, pady=(15, 5))

        columns_eval = ("titre", "note", "commentaire", "auteur")
        self.tree_eval = ttk.Treeview(self, columns=columns_eval, show="headings", selectmode="none")
        
        self.tree_eval.heading("titre", text="Résumé évalué")
        self.tree_eval.heading("note", text="Note")
        self.tree_eval.heading("commentaire", text="Commentaire")
        self.tree_eval.heading("auteur", text="Par")

        self.tree_eval.column("titre", width=200, anchor="w")
        self.tree_eval.column("note", width=50, anchor="center")
        self.tree_eval.column("commentaire", width=300, anchor="w")
        self.tree_eval.column("auteur", width=100, anchor="center")

        self.tree_eval.grid(row=5, column=0, sticky="nsew", padx=20, pady=(0, 20))

        scrollbar_eval = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.tree_eval.yview)
        self.tree_eval.configure(yscroll=scrollbar_eval.set)
        scrollbar_eval.grid(row=5, column=1, sticky="ns", pady=(0, 20))

        self.load_data()

    def load_data(self):
        """Récupère toutes les données et remplit les deux tableaux."""
        for item in self.tree.get_children():
            self.tree.delete(item)
        for item in self.tree_eval.get_children():
            self.tree_eval.delete(item)

        data = self.app_controller.get_library_data()

        for summary in data.get("my_summaries", []):
            self.tree.insert("", tk.END, values=(
                summary.id_resume, summary.titre, summary.code_cours, f"{float(summary.moyenne):.1f} / 5"
            ))

        for ev in data.get("my_evaluations", []):
            self.tree_eval.insert("", tk.END, values=(
                ev.titre_resume, f"{ev.note}/5", ev.commentaire, ev.nom_evaluateur
            ))

    def edit_selected(self):
        """Action pour modifier le résumé sélectionné via une fenêtre modale."""
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Sélection requise", "Sélectionnez le résumé à modifier.")
            return

        values = self.tree.item(selected_item[0], "values")
        summary_id = int(values[0])
        current_title = values[1]

        popup = tk.Toplevel(self)
        popup.title("Modifier le résumé")
        popup.geometry("400x300")
        popup.grab_set()

        tk.Label(popup, text="Nouveau titre :").pack(pady=(10, 0))
        title_entry = tk.Entry(popup, width=40)
        title_entry.insert(0, current_title)
        title_entry.pack(pady=5)

        tk.Label(popup, text="Nouveau contenu / description :").pack(pady=(10, 0))
        content_text = tk.Text(popup, width=40, height=8)
        content_text.pack(pady=5)

        def save_changes():
            new_title = title_entry.get().strip()
            new_content = content_text.get("1.0", tk.END).strip()
            
            success, msg = self.app_controller.modify_summary(summary_id, new_title, new_content)
            if success:
                messagebox.showinfo("Succès", msg)
                self.load_data()
                popup.destroy()
            else:
                messagebox.showerror("Erreur", msg)

        tk.Button(popup, text="Enregistrer", bg="green", fg="black", command=save_changes).pack(pady=10)

    def delete_selected(self):
        """Action déclenchée par le bouton Supprimer."""
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Sélection requise", "Veuillez d'abord cliquer sur un résumé dans le tableau.")
            return

        values = self.tree.item(selected_item[0], "values")
        summary_id = int(values[0])

        confirm = messagebox.askyesno("Attention", "Voulez-vous vraiment supprimer ce résumé de la base de données ?")
        if confirm:
            success, message = self.app_controller.remove_summary(summary_id)
            if success:
                self.load_data() 
            else:
                messagebox.showerror("Erreur", message)