"""
GUI Development: ttk.Treeview as a sortable, editable data table.
"""
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import csv
import io
from dataclasses import dataclass, fields, astuple
from typing import Any

# ═══════════════════════════════════════════
# Sample data model
# ═══════════════════════════════════════════
@dataclass
class Employee:
    id:         int
    name:       str
    department: str
    salary:     float
    years:      int

SAMPLE_DATA = [
    Employee(1,  "Alice Johnson",    "Engineering",  95000, 5),
    Employee(2,  "Bob Smith",        "Marketing",    72000, 3),
    Employee(3,  "Carol White",      "Engineering", 110000, 8),
    Employee(4,  "David Brown",      "HR",           65000, 2),
    Employee(5,  "Eva Martinez",     "Engineering",  98000, 6),
    Employee(6,  "Frank Davis",      "Finance",      88000, 4),
    Employee(7,  "Grace Wilson",     "Marketing",    76000, 5),
    Employee(8,  "Henry Lee",        "Engineering", 105000, 7),
    Employee(9,  "Iris Chen",        "HR",           67000, 1),
    Employee(10, "Jack Robinson",    "Finance",       92000, 9),
]

COLUMNS = [f.name for f in fields(Employee)]

# ═══════════════════════════════════════════
# Main application
# ═══════════════════════════════════════════
class DataTableApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Employee Data Table")
        self.geometry("900x600")

        self._sort_col: str = "id"
        self._sort_desc: bool = False
        self._rows: list[Employee] = list(SAMPLE_DATA)
        self._filter_var = tk.StringVar()
        self._filter_var.trace_add("write", lambda *_: self._apply_filter())

        self._build_ui()
        self._refresh()

    # ─────────────────────────────────────
    def _build_ui(self):
        # Top bar: filter + buttons
        top = ttk.Frame(self, padding=4)
        top.pack(fill=tk.X)

        ttk.Label(top, text="Search:").pack(side=tk.LEFT)
        ttk.Entry(top, textvariable=self._filter_var, width=25).pack(side=tk.LEFT, padx=4)

        for text, cmd in [
            ("Add Row",    self._add_row),
            ("Edit Row",   self._edit_row),
            ("Delete Row", self._delete_row),
            ("Export CSV", self._export_csv),
        ]:
            ttk.Button(top, text=text, command=cmd).pack(side=tk.LEFT, padx=2)

        self._count_label = ttk.Label(top, text="")
        self._count_label.pack(side=tk.RIGHT, padx=8)

        # Treeview with scrollbars
        frame = ttk.Frame(self)
        frame.pack(fill=tk.BOTH, expand=True, padx=4, pady=4)

        vsb = ttk.Scrollbar(frame, orient=tk.VERTICAL)
        hsb = ttk.Scrollbar(frame, orient=tk.HORIZONTAL)

        self.tree = ttk.Treeview(
            frame, columns=COLUMNS, show="headings",
            yscrollcommand=vsb.set, xscrollcommand=hsb.set,
        )
        vsb.config(command=self.tree.yview)
        hsb.config(command=self.tree.xview)

        vsb.pack(side=tk.RIGHT, fill=tk.Y)
        hsb.pack(side=tk.BOTTOM, fill=tk.X)
        self.tree.pack(fill=tk.BOTH, expand=True)

        # Configure columns
        widths = {"id": 50, "name": 180, "department": 130,
                  "salary": 100, "years": 80}
        for col in COLUMNS:
            self.tree.heading(col, text=col.capitalize(),
                              command=lambda c=col: self._sort(c))
            self.tree.column(col, width=widths.get(col, 100), anchor=tk.CENTER)

        # Double-click to edit
        self.tree.bind("<Double-1>", lambda e: self._edit_row())

        # Row striping
        self.tree.tag_configure("odd",  background="#f5f5f5")
        self.tree.tag_configure("even", background="white")
        self.tree.tag_configure("hi_salary", foreground="#1a7abf", font=("Arial", 10, "bold"))

        # Status bar
        self._status = tk.StringVar(value="Ready")
        ttk.Label(self, textvariable=self._status, relief=tk.SUNKEN,
                  anchor=tk.W).pack(fill=tk.X, side=tk.BOTTOM)

    # ─────────────────────────────────────
    def _refresh(self, rows: list[Employee] | None = None):
        if rows is None:
            rows = self._rows

        # Apply sort
        col = self._sort_col
        key_fn = {
            "id": lambda r: r.id, "name": lambda r: r.name,
            "department": lambda r: r.department,
            "salary": lambda r: r.salary, "years": lambda r: r.years,
        }.get(col, lambda r: r.id)
        rows = sorted(rows, key=key_fn, reverse=self._sort_desc)

        # Clear and repopulate
        self.tree.delete(*self.tree.get_children())
        for i, emp in enumerate(rows):
            tag = "odd" if i % 2 else "even"
            tags = [tag]
            if emp.salary >= 100_000:
                tags.append("hi_salary")
            self.tree.insert("", tk.END, iid=str(emp.id),
                             values=astuple(emp), tags=tags)

        self._count_label.configure(text=f"{len(rows)} rows")
        self._status.set(f"Showing {len(rows)}/{len(self._rows)} employees — "
                         f"sorted by {col} {'↓' if self._sort_desc else '↑'}")

    def _apply_filter(self):
        term = self._filter_var.get().lower()
        if not term:
            self._refresh()
            return
        filtered = [e for e in self._rows
                    if any(term in str(v).lower() for v in astuple(e))]
        self._refresh(filtered)

    def _sort(self, column: str):
        if self._sort_col == column:
            self._sort_desc = not self._sort_desc
        else:
            self._sort_col = column
            self._sort_desc = False
        self._apply_filter()

    # ─────────────────────────────────────
    def _selected_employee(self) -> Employee | None:
        sel = self.tree.selection()
        if not sel:
            messagebox.showinfo("Select Row", "Please select a row first.")
            return None
        emp_id = int(sel[0])
        return next((e for e in self._rows if e.id == emp_id), None)

    def _add_row(self):
        new_id = max((e.id for e in self._rows), default=0) + 1
        name = simpledialog.askstring("Add Employee", "Name:", parent=self)
        if not name: return
        dept = simpledialog.askstring("Add Employee", "Department:", parent=self)
        if not dept: return
        salary = simpledialog.askfloat("Add Employee", "Salary:", parent=self, minvalue=0)
        if salary is None: return
        years = simpledialog.askinteger("Add Employee", "Years:", parent=self, minvalue=0)
        if years is None: return
        self._rows.append(Employee(new_id, name, dept, salary, years))
        self._refresh()

    def _edit_row(self):
        emp = self._selected_employee()
        if not emp: return
        new_salary = simpledialog.askfloat(
            "Edit Salary", f"New salary for {emp.name}:",
            parent=self, initialvalue=emp.salary, minvalue=0
        )
        if new_salary is None: return
        idx = self._rows.index(emp)
        self._rows[idx] = Employee(emp.id, emp.name, emp.department, new_salary, emp.years)
        self._refresh()

    def _delete_row(self):
        emp = self._selected_employee()
        if not emp: return
        if messagebox.askyesno("Delete", f"Delete {emp.name}?"):
            self._rows.remove(emp)
            self._refresh()

    def _export_csv(self):
        buf = io.StringIO()
        w = csv.DictWriter(buf, fieldnames=COLUMNS)
        w.writeheader()
        for emp in self._rows:
            w.writerow(emp.__dict__)
        print("=== CSV Export ===")
        print(buf.getvalue())
        messagebox.showinfo("Exported", "CSV exported to console.")

if __name__ == "__main__":
    print("Launch data table app (close window to exit)...")
    DataTableApp().mainloop()
