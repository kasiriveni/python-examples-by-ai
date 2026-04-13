"""
GUI Development: Dialogs, menus, and file choosers in Tkinter.
"""
import tkinter as tk
from tkinter import ttk, messagebox, filedialog, simpledialog, colorchooser

class MenuApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Menus, Dialogs & File Chooser")
        self.geometry("600x450")
        self._file_content = ""
        self._build_menu()
        self._build_ui()

    # ──────────────────────────────────────
    # Menu Bar
    # ──────────────────────────────────────
    def _build_menu(self):
        menubar = tk.Menu(self)
        self.config(menu=menubar)

        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New",       command=self.new_file,  accelerator="Ctrl+N")
        file_menu.add_command(label="Open...",   command=self.open_file, accelerator="Ctrl+O")
        file_menu.add_command(label="Save As...", command=self.save_file)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.on_exit)

        # Edit menu
        edit_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Edit", menu=edit_menu)
        edit_menu.add_command(label="Copy",  command=self.copy_text,  accelerator="Ctrl+C")
        edit_menu.add_command(label="Paste", command=self.paste_text, accelerator="Ctrl+V")
        edit_menu.add_separator()
        edit_menu.add_command(label="Font Size...", command=self.ask_font_size)

        # View menu with checkbutton / radiobutton
        view_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="View", menu=view_menu)
        self._show_status = tk.BooleanVar(value=True)
        view_menu.add_checkbutton(label="Status Bar", variable=self._show_status,
                                   command=self._toggle_status)
        self._theme = tk.StringVar(value="light")
        for t in ("light", "dark", "solarized"):
            view_menu.add_radiobutton(label=t.title(), variable=self._theme, value=t,
                                       command=lambda: self._apply_theme())

        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)

        # Keyboard shortcuts
        self.bind("<Control-n>", lambda e: self.new_file())
        self.bind("<Control-o>", lambda e: self.open_file())

    # ──────────────────────────────────────
    # Main UI
    # ──────────────────────────────────────
    def _build_ui(self):
        # Toolbar
        toolbar = ttk.Frame(self, relief=tk.RIDGE)
        toolbar.pack(fill=tk.X, side=tk.TOP)
        for label, cmd in [("New", self.new_file), ("Open", self.open_file),
                            ("Color", self.pick_color), ("Msg", self.show_dialogs)]:
            ttk.Button(toolbar, text=label, command=cmd, width=7).pack(side=tk.LEFT, padx=2, pady=2)

        # Text area
        self._text = tk.Text(self, wrap=tk.WORD, font=("Courier", 11))
        self._text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self._text.insert(tk.END, "Welcome! Use the menus and toolbar to explore dialogs.\n")

        # Status bar
        self._status_var = tk.StringVar(value="Ready")
        self._statusbar = ttk.Label(self, textvariable=self._status_var,
                                     relief=tk.SUNKEN, anchor=tk.W)
        self._statusbar.pack(fill=tk.X, side=tk.BOTTOM)

        # Right-click context menu
        self._context = tk.Menu(self, tearoff=0)
        self._context.add_command(label="Cut",   command=self.cut_text)
        self._context.add_command(label="Copy",  command=self.copy_text)
        self._context.add_command(label="Paste", command=self.paste_text)
        self._text.bind("<Button-3>", self._show_context)

    def _show_context(self, event):
        self._context.post(event.x_root, event.y_root)

    # ──────────────────────────────────────
    # Dialog Actions
    # ──────────────────────────────────────
    def new_file(self):
        if self._text.get("1.0", tk.END).strip():
            if not messagebox.askyesno("New File", "Discard changes?"):
                return
        self._text.delete("1.0", tk.END)
        self._status("New file created")

    def open_file(self):
        path = filedialog.askopenfilename(
            filetypes=[("Python", "*.py"), ("Text", "*.txt"), ("All", "*.*")])
        if path:
            try:
                with open(path, encoding="utf-8") as f:
                    content = f.read()
                self._text.delete("1.0", tk.END)
                self._text.insert(tk.END, content)
                self._status(f"Opened: {path}")
            except OSError as e:
                messagebox.showerror("Error", str(e))

    def save_file(self):
        path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text", "*.txt"), ("Python", "*.py"), ("All", "*.*")])
        if path:
            try:
                with open(path, "w", encoding="utf-8") as f:
                    f.write(self._text.get("1.0", tk.END))
                self._status(f"Saved: {path}")
            except OSError as e:
                messagebox.showerror("Error", str(e))

    def show_dialogs(self):
        messagebox.showinfo("Info",    "showinfo dialog")
        messagebox.showwarning("Warn", "showwarning dialog")
        choice = messagebox.askyesnocancel("Question", "Yes, No, or Cancel?")
        self._status(f"Dialog choice: {choice}")

    def ask_font_size(self):
        size = simpledialog.askinteger("Font Size", "Enter size (8-72):", minvalue=8, maxvalue=72)
        if size:
            self._text.config(font=("Courier", size))
            self._status(f"Font size: {size}")

    def pick_color(self):
        color = colorchooser.askcolor(title="Pick a color")
        if color[1]:
            self._text.config(bg=color[1])
            self._status(f"Color: {color[1]}")

    def show_about(self):
        messagebox.showinfo("About", "Tkinter Dialogs & Menus\nPython GUI demo")

    def copy_text(self):
        self._text.event_generate("<<Copy>>")

    def cut_text(self):
        self._text.event_generate("<<Cut>>")

    def paste_text(self):
        self._text.event_generate("<<Paste>>")

    def on_exit(self):
        if messagebox.askokcancel("Exit", "Really exit?"):
            self.destroy()

    def _toggle_status(self):
        if self._show_status.get():
            self._statusbar.pack(fill=tk.X, side=tk.BOTTOM)
        else:
            self._statusbar.pack_forget()

    def _apply_theme(self):
        themes = {"light": ("white", "black"), "dark": ("#1e1e1e", "#d4d4d4"),
                  "solarized": ("#fdf6e3", "#657b83")}
        bg, fg = themes.get(self._theme.get(), ("white", "black"))
        self._text.config(bg=bg, fg=fg, insertbackground=fg)
        self._status(f"Theme: {self._theme.get()}")

    def _status(self, msg: str):
        self._status_var.set(msg)
        print(f"  [Status] {msg}")

if __name__ == "__main__":
    print("Launching Menus & Dialogs app...")
    app = MenuApp()
    app.mainloop()
