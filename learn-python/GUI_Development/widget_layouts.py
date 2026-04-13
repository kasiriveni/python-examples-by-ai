"""
GUI Development: Tkinter widget layouts.
Covers Pack, Grid, Place geometry managers and common widgets.
"""
import tkinter as tk
from tkinter import ttk

def demonstrate_pack():
    """Demo: Pack geometry manager."""
    root = tk.Tk()
    root.title("Pack Layout Demo")
    root.geometry("400x300")

    # Top bar
    header = tk.Frame(root, bg="navy", height=50)
    header.pack(fill=tk.X, side=tk.TOP)
    tk.Label(header, text="Header", bg="navy", fg="white",
             font=("Arial", 14, "bold")).pack(pady=10)

    # Sidebar
    sidebar = tk.Frame(root, bg="#2ecc71", width=100)
    sidebar.pack(fill=tk.Y, side=tk.LEFT)
    for item in ["Home", "About", "Settings"]:
        tk.Button(sidebar, text=item, width=10).pack(pady=5, padx=5)

    # Main content
    main = tk.Frame(root, bg="white")
    main.pack(fill=tk.BOTH, expand=True)
    tk.Label(main, text="Main Content Area", font=("Arial", 12)).pack(expand=True)

    # Bottom
    footer = tk.Frame(root, bg="#bdc3c7", height=30)
    footer.pack(fill=tk.X, side=tk.BOTTOM)
    tk.Label(footer, text="Footer", bg="#bdc3c7").pack(pady=5)

    return root

def demonstrate_grid():
    """Demo: Grid geometry manager (form layout)."""
    root = tk.Tk()
    root.title("Grid Layout - Login Form")
    root.geometry("350x250")

    frame = ttk.LabelFrame(root, text="Login", padding=20)
    frame.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

    fields = ["Username", "Password", "Email"]
    entries = {}

    for row, label in enumerate(fields):
        ttk.Label(frame, text=label + ":").grid(row=row, column=0, sticky=tk.W, pady=5)
        entry = ttk.Entry(frame, width=25,
                          show="*" if label == "Password" else "")
        entry.grid(row=row, column=1, pady=5, padx=(10, 0))
        entries[label] = entry

    # Buttons row
    btn_frame = ttk.Frame(frame)
    btn_frame.grid(row=len(fields), column=0, columnspan=2, pady=15)

    ttk.Button(btn_frame, text="Login").pack(side=tk.LEFT, padx=5)
    ttk.Button(btn_frame, text="Cancel").pack(side=tk.LEFT, padx=5)
    ttk.Button(btn_frame, text="Sign Up").pack(side=tk.LEFT, padx=5)

    return root

def demonstrate_place():
    """Demo: Place geometry manager (absolute positioning)."""
    root = tk.Tk()
    root.title("Place Layout Demo")
    root.geometry("400x300")

    # Absolute positioning
    tk.Label(root, text="Absolute layout:", font=("Arial", 11, "bold")).place(x=10, y=10)
    tk.Button(root, text="Top-Left").place(x=10, y=40)
    tk.Button(root, text="Center").place(relx=0.5, rely=0.5, anchor=tk.CENTER)
    tk.Button(root, text="Bottom-Right").place(relx=1.0, rely=1.0, anchor=tk.SE, x=-10, y=-10)

    # Relative positioning
    info = tk.Label(root, text="relx=0.5, rely=0.2", bg="yellow")
    info.place(relx=0.5, rely=0.2, anchor=tk.N)

    return root

def demonstrate_widgets():
    """Demo: Common Tkinter widgets."""
    root = tk.Tk()
    root.title("Widget Gallery")
    root.geometry("500x600")
    root.resizable(True, True)

    notebook = ttk.Notebook(root)
    notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    # --- Tab 1: Basic Widgets ---
    tab1 = ttk.Frame(notebook)
    notebook.add(tab1, text="Basic")

    ttk.Label(tab1, text="Label widget", font=("Arial", 12)).pack(pady=5)
    ttk.Button(tab1, text="Click Me", command=lambda: print("Clicked!")).pack(pady=5)
    ttk.Entry(tab1, width=30).pack(pady=5)

    text = tk.Text(tab1, height=4, width=40)
    text.pack(pady=5)
    text.insert(tk.END, "Text widget\nSupports multiple lines\n")

    # --- Tab 2: Selection Widgets ---
    tab2 = ttk.Frame(notebook)
    notebook.add(tab2, text="Selection")

    var_check = tk.BooleanVar(value=True)
    ttk.Checkbutton(tab2, text="Checkbox", variable=var_check).pack(pady=3)

    var_radio = tk.StringVar(value="option1")
    for opt in ["option1", "option2", "option3"]:
        ttk.Radiobutton(tab2, text=opt.title(), variable=var_radio, value=opt).pack(anchor=tk.W, padx=20)

    ttk.Label(tab2, text="Combobox:").pack(pady=(10, 0))
    combo = ttk.Combobox(tab2, values=["Python", "JavaScript", "Rust", "Go"])
    combo.pack(pady=3)
    combo.set("Python")

    ttk.Label(tab2, text="Listbox:").pack(pady=(10, 0))
    lb = tk.Listbox(tab2, height=4, width=20)
    for item in ["Item A", "Item B", "Item C", "Item D"]:
        lb.insert(tk.END, item)
    lb.pack(pady=3)

    # --- Tab 3: Range Widgets ---
    tab3 = ttk.Frame(notebook)
    notebook.add(tab3, text="Ranges")

    ttk.Label(tab3, text="Scale (slider):").pack(pady=5)
    scale_var = tk.DoubleVar(value=50)
    ttk.Scale(tab3, variable=scale_var, from_=0, to=100, length=200).pack()
    ttk.Label(tab3, textvariable=scale_var).pack()

    ttk.Label(tab3, text="Progressbar:").pack(pady=(15, 5))
    progress = ttk.Progressbar(tab3, length=200, mode="determinate", value=65)
    progress.pack()

    ttk.Label(tab3, text="Spinbox:").pack(pady=(15, 5))
    ttk.Spinbox(tab3, from_=0, to=100, width=10).pack()

    return root

# Run whichever demo you want:
if __name__ == "__main__":
    print("Launching widget gallery (close window to exit)...")
    root = demonstrate_widgets()
    root.mainloop()
