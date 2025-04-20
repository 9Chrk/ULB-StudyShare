from core import user
import tkinter as tk
from tkinter import ttk, font, messagebox

class App:
  def __init__(self, root):
    self.root = root
    self.root.title("KingdomDB")
    
    width = 500
    height = 600
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    offset_x = (screen_width - width) // 2
    offset_y = (screen_height - height) // 2
    root.geometry(f"{width}x{height}+{offset_x}+{offset_y}")

    self.font = font.nametofont("TkDefaultFont")
    self.font.configure(family="Segoe UI", size=10)

    self.style = ttk.Style()
    self.style.configure("TLabel", font=("Segoe UI", 10))
    self.style.configure("TButton", font=("Segoe UI", 10))
    self.style.configure("TEntry", font=("Segoe UI", 10))

    self.root.configure(bg="#1a1a2e")
    
    self.login_menu()
  
  
  # ------------------------------- LOGIN MENU ------------------------------- 
  
  def login_menu(self):
    for widget in self.root.winfo_children():
      if isinstance(widget, tk.Frame):
        widget.destroy()
            
    login_frame = tk.Frame(self.root, bg="white", bd=0)
    login_frame.place(relx=0.5, rely=0.5, width=350, height=320, anchor="center")
    
    # Close button
    close_button = tk.Label(login_frame, text="×", font=("Arial", 16), bg="white", fg="#999", cursor="hand2")
    close_button.place(x=320, y=10)
    close_button.bind("<Button-1>", lambda _: self.root.destroy())
    
    # Title
    title_label = tk.Label(login_frame, text="KingdomDB", font=("Segoe UI", 20, "bold"), bg="white")
    title_label.place(relx=0.5, y=40, anchor="center")
    
    # Sub-title
    subtitle_label = tk.Label(login_frame, text="Where every hero carves their own legend.", font=("Segoe UI", 10), bg="white", fg="#666")
    subtitle_label.place(relx=0.5, y=70, anchor="center")
    
    # Username field
    user_icon = tk.Label(login_frame, text="👤", font=("Segoe UI", 12), bg="white")
    user_icon.place(x=20, y=110)
    user_entry = ttk.Entry(login_frame, font=("Segoe UI", 10))
    user_entry.insert(0, "Username")
    user_entry.place(x=50, y=110, width=270, height=30)
    
    # Password field
    password_icon = tk.Label(login_frame, text="🔒", font=("Segoe UI", 12), bg="white")
    password_icon.place(x=20, y=160)
    password_entry = ttk.Entry(login_frame, font=("Segoe UI", 10))
    password_entry.insert(0, "Password")
    password_entry.place(x=50, y=160, width=270, height=30)
    
    # Connect button
    login_button = tk.Button(login_frame, text="Log in", font=("Segoe UI", 10, "bold"), bg="#00d68f", fg="white", bd=0, cursor="hand2")
    login_button.place(x=30, y=210, width=290, height=40)
    login_button.bind("<Button-1>", lambda _: self.login(user_entry, password_entry))
    
    # Register link
    register_label = tk.Label(login_frame, text="New user? ", font=("Segoe UI", 9), bg="white", fg="#999")
    register_label.place(x=70, y=270)
    
    register_link = tk.Label(login_frame, text="Create an account", font=("Segoe UI", 9, "underline"), bg="white", fg="#00d68f", cursor="hand2")
    register_link.place(x=130, y=270)
    register_link.bind("<Button-1>", lambda _: self.register_menu())
    
    # Handle focus events for fields
    self.entry_behavior(user_entry, "Username")
    self.entry_behavior(password_entry, "Password", is_password=True)
  
  
  # ------------------------------- REGISTRATION MENU -------------------------------
  
  def register_menu(self):
    for widget in self.root.winfo_children():
      if isinstance(widget, tk.Frame):
        widget.destroy()
    
    register_frame = tk.Frame(self.root, bg="white", bd=0)
    register_frame.place(relx=0.5, rely=0.5, width=350, height=370, anchor="center")
    
    # Close button
    close_button = tk.Label(register_frame, text="×", font=("Arial", 16), bg="white", fg="#999", cursor="hand2")
    close_button.place(x=320, y=10)
    close_button.bind("<Button-1>", lambda _: self.root.destroy())
    
    # Title
    title_label = tk.Label(register_frame, text="Create Account", font=("Segoe UI", 20, "bold"), bg="white")
    title_label.place(relx=0.5, y=40, anchor="center")
    
    # Sub-title
    subtitle_label = tk.Label(register_frame, text="Join the Kingdom's adventure", font=("Segoe UI", 10), bg="white", fg="#666")
    subtitle_label.place(relx=0.5, y=70, anchor="center")
    
    # Username field
    user_icon = tk.Label(register_frame, text="👤", font=("Segoe UI", 12), bg="white")
    user_icon.place(x=20, y=110)
    user_entry = ttk.Entry(register_frame, font=("Segoe UI", 10))
    user_entry.insert(0, "Username")
    user_entry.place(x=50, y=110, width=270, height=30)
    
    # Password field
    password_icon = tk.Label(register_frame, text="🔒", font=("Segoe UI", 12), bg="white")
    password_icon.place(x=20, y=160)
    password_entry = ttk.Entry(register_frame, font=("Segoe UI", 10))
    password_entry.insert(0, "Password")
    password_entry.place(x=50, y=160, width=270, height=30)
    
    # Confirm Password field
    confirm_icon = tk.Label(register_frame, text="🔒", font=("Segoe UI", 12), bg="white")
    confirm_icon.place(x=20, y=210)
    confirm_password_entry = ttk.Entry(register_frame, font=("Segoe UI", 10))
    confirm_password_entry.insert(0, "Confirm Password")
    confirm_password_entry.place(x=50, y=210, width=270, height=30)
    
    # Create Account button
    register_button = tk.Button(register_frame, text="Create Account", font=("Segoe UI", 10, "bold"), bg="#00d68f", fg="white", bd=0, cursor="hand2")
    register_button.place(x=30, y=260, width=290, height=40)
    register_button.bind("<Button-1>", lambda _: self.register(user_entry, password_entry, confirm_password_entry))
    
    # Login link
    login_label = tk.Label(register_frame, text="Already have an account? ", font=("Segoe UI", 9), bg="white", fg="#999")
    login_label.place(x=70, y=320)
    
    login_link = tk.Label(register_frame, text="Log in", font=("Segoe UI", 9, "underline"), bg="white", fg="#00d68f", cursor="hand2")
    login_link.place(x=210, y=320)
    login_link.bind("<Button-1>", lambda _: self.login_menu())
    
    # Handle focus events for fields
    self.entry_behavior(user_entry, "Username")
    self.entry_behavior(password_entry, "Password", is_password=True)
    self.entry_behavior(confirm_password_entry, "Confirm Password", is_password=True)
  
  
  # ------------------------------- COMMON -------------------------------
  
  def entry_behavior(self, entry, placeholder, is_password=False):
    def focus_in(event):
      if entry.get() == placeholder:
        entry.delete(0, tk.END)
        if is_password:
          entry.config(show="•")
    
    def focus_out(event):
      if entry.get() == "":
        entry.insert(0, placeholder)
        if is_password:
          entry.config(show="")
    
    entry.bind("<FocusIn>", focus_in)
    entry.bind("<FocusOut>", focus_out)
  
  
  def login(self, user_entry, password_entry):
    username = user_entry.get()
    password = password_entry.get()
    
    password_entry.delete(0, tk.END)
    if user.check(username, password):
      user_entry.delete(0, tk.END)
      self.alert("Login successful!")
    else:
      self.alert("Invalid username or password.", error=True)
    
    
  def register(self, user_entry, password_entry, confirm_password_entry):
    username = user_entry.get()
    password = password_entry.get()
    confirm_password = confirm_password_entry.get()
    
    password_entry.delete(0, tk.END)
    confirm_password_entry.delete(0, tk.END)
    
    if password == confirm_password:
      user_entry.delete(0, tk.END)
      user.add(username, password)
      self.alert("Registration successful!")
      self.login_menu()
    else:
      self.alert("Passwords do not match.", error=True)
  
  
  def alert(self, message, error=False):
    if error:
      messagebox.showerror("Error", message, parent=self.root)
    else:
      messagebox.showinfo("Info", message, parent=self.root)
