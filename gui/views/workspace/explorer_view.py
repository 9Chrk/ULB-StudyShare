import tkinter as tk
from tkinter import ttk, messagebox

class ExplorerView(tk.Frame):
    def __init__(self, master, app_controller, **kwargs):
        bg_color = kwargs.pop('bg', 'white')
        super().__init__(master, **kwargs)
        self.app_controller = app_controller
        self.configure(bg=bg_color)
        
        self.rowconfigure(2, weight=1)
        self.columnconfigure(0, weight=1) # Colonne gauche (Cours)
        self.columnconfigure(1, weight=2) # Colonne droite (Résumés)

        # En-tête
        tk.Label(self, text="Explorateur de Cours", font=("Helvetica", 24, "bold"), bg=bg_color).grid(row=0, column=0, columnspan=2, sticky="w", padx=20, pady=(20, 5))

        # partie gauche : 
        left_frame = tk.Frame(self, bg=bg_color)
        left_frame.grid(row=2, column=0, sticky="nsew", padx=20, pady=10)
        left_frame.rowconfigure(2, weight=1)
        left_frame.columnconfigure(0, weight=1)

        search_frame = tk.Frame(left_frame, bg=bg_color)
        search_frame.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        self.search_var = tk.StringVar()
        tk.Entry(search_frame, textvariable=self.search_var).pack(side="left", fill="x", expand=True, padx=(0, 5))
        tk.Button(search_frame, text="Chercher", command=self.load_courses).pack(side="left")
        tk.Button(search_frame, text="+ Cours", fg="green", command=self.popup_add_course).pack(side="left", padx=5)

        self.tree_courses = ttk.Treeview(left_frame, columns=("code", "nom"), show="headings", selectmode="browse")
        self.tree_courses.heading("code", text="Code")
        self.tree_courses.heading("nom", text="Cours")
        self.tree_courses.column("code", width=80)
        self.tree_courses.column("nom", width=200)
        self.tree_courses.grid(row=2, column=0, sticky="nsew")
        self.tree_courses.bind("<<TreeviewSelect>>", self.on_course_select)

        # partie droite : 
        right_frame = tk.Frame(self, bg=bg_color)
        right_frame.grid(row=2, column=1, sticky="nsew", padx=20, pady=10)
        right_frame.rowconfigure(1, weight=1)
        right_frame.columnconfigure(0, weight=1)

        header_res = tk.Frame(right_frame, bg=bg_color)
        header_res.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        self.lbl_selected_course = tk.Label(header_res, text="Sélectionnez un cours", font=("Helvetica", 14, "bold"), bg=bg_color)
        self.lbl_selected_course.pack(side="left")
        self.btn_publish = tk.Button(header_res, text="Publier un résumé", fg="blue", state="disabled", command=self.popup_publish)
        self.btn_publish.pack(side="right")

        self.tree_summaries = ttk.Treeview(right_frame, columns=("id", "titre", "auteur", "note"), show="headings", selectmode="browse")
        self.tree_summaries.heading("id", text="ID")
        self.tree_summaries.heading("titre", text="Titre")
        self.tree_summaries.heading("auteur", text="Auteur")
        self.tree_summaries.heading("note", text="Note")
        self.tree_summaries.column("id", width=0, stretch=tk.NO)
        self.tree_summaries.column("note", width=60, anchor="center")
        self.tree_summaries.grid(row=1, column=0, sticky="nsew")

        tk.Button(right_frame, text="Évaluer ce résumé", command=self.popup_evaluate).grid(row=2, column=0, sticky="e", pady=10)

        self.current_course_id = None
        self.load_courses()

    def load_courses(self):
        for i in self.tree_courses.get_children(): self.tree_courses.delete(i)
        query = self.search_var.get()
        courses = self.app_controller.explorer_service.get_courses(query) 
        for c in courses:
            self.tree_courses.insert("", tk.END, values=(c.code_cours, c.nom_cours))

    def on_course_select(self, event):
        sel = self.tree_courses.selection()
        if not sel: return
        self.current_course_id = self.tree_courses.item(sel[0], "values")[0]
        self.lbl_selected_course.config(text=f"Résumés pour : {self.current_course_id}")
        self.btn_publish.config(state="normal")
        self.load_summaries()

    def load_summaries(self):
        for i in self.tree_summaries.get_children(): self.tree_summaries.delete(i)
        if not self.current_course_id: return
        summaries = self.app_controller.explorer_service.get_summaries_for_course(self.current_course_id)
        for s in summaries:
            self.tree_summaries.insert("", tk.END, values=(s.id_resume, s.titre, s.auteur, f"{s.moyenne:.1f}/5 ({s.nb_eval} avis)"))

    def popup_add_course(self):
        p = tk.Toplevel(self)
        p.title("Nouveau Cours"); p.geometry("300x250"); p.grab_set()
        tk.Label(p, text="Code (ex: INFO-F201):").pack(pady=5); c_entry = tk.Entry(p); c_entry.pack()
        tk.Label(p, text="Nom:").pack(pady=5); n_entry = tk.Entry(p); n_entry.pack()
        tk.Label(p, text="Faculté:").pack(pady=5); f_entry = tk.Entry(p); f_entry.pack()
        def save():
            ok, msg = self.app_controller.explorer_service.add_course(c_entry.get(), n_entry.get(), f_entry.get())
            if ok: messagebox.showinfo("Succès", msg); self.load_courses(); p.destroy()
            else: messagebox.showerror("Erreur", msg)
        tk.Button(p, text="Ajouter", bg="green", command=save).pack(pady=15)

    def popup_publish(self):
        p = tk.Toplevel(self)
        p.title("Publier un résumé")
        p.geometry("400x400")
        p.grab_set()
        
        tk.Label(
            p, text=f"📌 Résumé lié au cours : {self.current_course_id}", 
            font=("Helvetica", 12, "bold"), fg="blue"
        ).pack(pady=(15, 10))

        tk.Label(p, text="Titre du résumé :").pack(pady=0)
        t_entry = tk.Entry(p, width=40)
        t_entry.pack(pady=5)
        
        tk.Label(p, text="Année académique :").pack(pady=0)
        annees_db = self.app_controller.get_academic_years()
        
        # au cas ou la table est vide
        if not annees_db:
            annees_db = ["Table AnneeAcademique vide !"]
            
        y_combo = ttk.Combobox(p, values=annees_db, state="readonly", width=37)
        y_combo.set(annees_db[0]) # Sélectionne la première année par défaut
        y_combo.pack(pady=5)

        tk.Label(p, text="Contenu / Description :").pack(pady=0)
        c_text = tk.Text(p, width=40, height=6)
        c_text.pack(pady=5)
        
        def save():
            ok, msg = self.app_controller.publish_summary(
                self.current_course_id, t_entry.get(), c_text.get("1.0", tk.END), y_combo.get()
            )
            if ok: 
                messagebox.showinfo("Succès", msg)
                self.load_summaries()
                p.destroy()
            else: 
                messagebox.showerror("Erreur", msg)
                
        tk.Button(p, text="Publier mon résumé", bg="green", fg="black", command=save).pack(pady=10)

    def popup_evaluate(self):
        sel = self.tree_summaries.selection()
        if not sel: return messagebox.showwarning("Erreur", "Sélectionnez un résumé.")
        s_id = int(self.tree_summaries.item(sel[0], "values")[0])
        p = tk.Toplevel(self)
        p.title("Évaluer"); p.geometry("300x250"); p.grab_set()
        tk.Label(p, text="Note (1 à 5):").pack(pady=5); n_entry = tk.Entry(p); n_entry.pack()
        tk.Label(p, text="Commentaire:").pack(pady=5); c_entry = tk.Entry(p); c_entry.pack()
        def save():
            try: note = int(n_entry.get())
            except: return messagebox.showerror("Erreur", "Note invalide.")
            ok, msg = self.app_controller.rate_summary(s_id, note, c_entry.get())
            if ok: messagebox.showinfo("Succès", msg); self.load_summaries(); p.destroy()
            else: messagebox.showerror("Erreur", msg)
        tk.Button(p, text="Envoyer", command=save).pack(pady=15)