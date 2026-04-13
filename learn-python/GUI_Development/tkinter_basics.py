"""
GUI Development: Tkinter basics - windows, widgets, and layouts.
"""
import tkinter as tk
from tkinter import ttk, messagebox

# === Example 1: Hello World Window ===
def hello_world_app():
    """Simplest Tkinter application."""
    root = tk.Tk()
    root.title("Hello World")
    root.geometry("300x200")

    label = tk.Label(root, text="Hello, Tkinter!", font=("Arial", 16))
    label.pack(pady=50)

    button = tk.Button(root, text="Quit", command=root.quit)
    button.pack()

    # root.mainloop()  # Uncomment to run
    return root

# === Example 2: Calculator ===
class Calculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculator")
        self.expression = ""

        self.display = tk.Entry(root, font=("Arial", 18), justify="right", bd=5)
        self.display.grid(row=0, column=0, columnspan=4, sticky="nsew", padx=5, pady=5)

        buttons = [
            '7', '8', '9', '/',
            '4', '5', '6', '*',
            '1', '2', '3', '-',
            'C', '0', '=', '+',
        ]

        for i, btn_text in enumerate(buttons):
            row = i // 4 + 1
            col = i % 4
            btn = tk.Button(root, text=btn_text, font=("Arial", 14), width=5, height=2,
                          command=lambda t=btn_text: self.on_click(t))
            btn.grid(row=row, column=col, padx=2, pady=2)

    def on_click(self, char):
        if char == 'C':
            self.expression = ""
        elif char == '=':
            try:
                self.expression = str(eval(self.expression))
            except Exception:
                self.expression = "Error"
        else:
            self.expression += char
        self.display.delete(0, tk.END)
        self.display.insert(0, self.expression)

# === Example 3: Todo List ===
class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Todo List")
        self.root.geometry("400x500")

        # Input frame
        input_frame = tk.Frame(root)
        input_frame.pack(fill="x", padx=10, pady=10)

        self.entry = tk.Entry(input_frame, font=("Arial", 12))
        self.entry.pack(side="left", fill="x", expand=True)
        self.entry.bind("<Return>", lambda e: self.add_task())

        add_btn = tk.Button(input_frame, text="Add", command=self.add_task)
        add_btn.pack(side="right", padx=(5, 0))

        # Task list
        self.listbox = tk.Listbox(root, font=("Arial", 12), selectmode="single")
        self.listbox.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        # Buttons
        btn_frame = tk.Frame(root)
        btn_frame.pack(fill="x", padx=10, pady=(0, 10))

        tk.Button(btn_frame, text="Complete", command=self.complete_task).pack(side="left")
        tk.Button(btn_frame, text="Delete", command=self.delete_task).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Clear All", command=self.clear_all).pack(side="right")

    def add_task(self):
        task = self.entry.get().strip()
        if task:
            self.listbox.insert(tk.END, task)
            self.entry.delete(0, tk.END)

    def complete_task(self):
        selection = self.listbox.curselection()
        if selection:
            idx = selection[0]
            task = self.listbox.get(idx)
            self.listbox.delete(idx)
            self.listbox.insert(idx, f"✓ {task}")
            self.listbox.itemconfig(idx, fg="gray")

    def delete_task(self):
        selection = self.listbox.curselection()
        if selection:
            self.listbox.delete(selection[0])

    def clear_all(self):
        if messagebox.askyesno("Confirm", "Clear all tasks?"):
            self.listbox.delete(0, tk.END)

# === Example 4: Form with validation ===
class RegistrationForm:
    def __init__(self, root):
        self.root = root
        self.root.title("Registration")

        fields = [("Name", "name"), ("Email", "email"), ("Age", "age")]
        self.entries = {}

        for i, (label, key) in enumerate(fields):
            tk.Label(root, text=f"{label}:").grid(row=i, column=0, padx=10, pady=5, sticky="e")
            entry = tk.Entry(root)
            entry.grid(row=i, column=1, padx=10, pady=5, sticky="ew")
            self.entries[key] = entry

        tk.Button(root, text="Submit", command=self.submit).grid(
            row=len(fields), column=0, columnspan=2, pady=10
        )

    def submit(self):
        data = {k: e.get() for k, e in self.entries.items()}
        errors = []
        if not data["name"]:
            errors.append("Name is required")
        if "@" not in data.get("email", ""):
            errors.append("Valid email is required")
        try:
            age = int(data["age"])
            if age < 0 or age > 150:
                errors.append("Age must be between 0-150")
        except ValueError:
            errors.append("Age must be a number")

        if errors:
            messagebox.showerror("Errors", "\n".join(errors))
        else:
            messagebox.showinfo("Success", f"Registered: {data['name']}")

if __name__ == "__main__":
    print("GUI Examples (uncomment mainloop to run):")
    print("1. Hello World")
    print("2. Calculator")
    print("3. Todo App")
    print("4. Registration Form")

    # Uncomment one to run:
    # root = tk.Tk(); Calculator(root); root.mainloop()
    # root = tk.Tk(); TodoApp(root); root.mainloop()
    # root = tk.Tk(); RegistrationForm(root); root.mainloop()
