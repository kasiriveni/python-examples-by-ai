"""
GUI Development: Tkinter custom widgets — reusable components.
"""
import tkinter as tk
from tkinter import ttk, font

# ═══════════════════════════════════════════
# 1. Tooltip (hover popup)
# ═══════════════════════════════════════════
class Tooltip:
    """Show a tooltip popup when hovering over a widget."""

    def __init__(self, widget: tk.Widget, text: str, delay: int = 500):
        self._widget = widget
        self._text = text
        self._delay = delay
        self._popup: tk.Toplevel | None = None
        self._after_id: str | None = None

        widget.bind("<Enter>",  self._schedule)
        widget.bind("<Leave>",  self._cancel)
        widget.bind("<Button>", self._cancel)

    def _schedule(self, _event=None):
        self._after_id = self._widget.after(self._delay, self._show)

    def _cancel(self, _event=None):
        if self._after_id:
            self._widget.after_cancel(self._after_id)
            self._after_id = None
        self._hide()

    def _show(self):
        if self._popup:
            return
        x = self._widget.winfo_rootx() + self._widget.winfo_width() // 2
        y = self._widget.winfo_rooty() + self._widget.winfo_height() + 4
        self._popup = tw = tk.Toplevel(self._widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x}+{y}")
        label = tk.Label(tw, text=self._text, justify="left",
                         background="#ffff88", relief="solid", borderwidth=1,
                         font=("TkDefaultFont", 9))
        label.pack()

    def _hide(self):
        if self._popup:
            self._popup.destroy()
            self._popup = None

# ═══════════════════════════════════════════
# 2. Star rating widget
# ═══════════════════════════════════════════
class StarRating(tk.Frame):
    """Clickable ★ star rating widget."""

    def __init__(self, master, max_stars: int = 5, initial: int = 0,
                 on_change=None, **kw):
        super().__init__(master, **kw)
        self._max = max_stars
        self._value = initial
        self._on_change = on_change
        self._labels: list[tk.Label] = []
        self._build()

    def _build(self):
        for i in range(1, self._max + 1):
            lbl = tk.Label(self, text="★", font=("TkDefaultFont", 18),
                           cursor="hand2")
            lbl.grid(row=0, column=i - 1, padx=1)
            lbl.bind("<Button-1>", lambda e, v=i: self.set(v))
            lbl.bind("<Enter>",    lambda e, v=i: self._hover(v))
            lbl.bind("<Leave>",    lambda e: self._render(self._value))
            self._labels.append(lbl)
        self._render(self._value)

    def _render(self, highlighted: int):
        for i, lbl in enumerate(self._labels, 1):
            lbl.config(foreground="#FFD700" if i <= highlighted else "#CCCCCC")

    def _hover(self, value: int):
        self._render(value)

    def set(self, value: int):
        self._value = max(0, min(value, self._max))
        self._render(self._value)
        if self._on_change:
            self._on_change(self._value)

    @property
    def value(self) -> int:
        return self._value

# ═══════════════════════════════════════════
# 3. Toggle switch
# ═══════════════════════════════════════════
class ToggleSwitch(tk.Canvas):
    """macOS-style toggle switch."""

    WIDTH, HEIGHT = 46, 24

    def __init__(self, master, variable: tk.BooleanVar | None = None,
                 on_change=None, **kw):
        super().__init__(master, width=self.WIDTH, height=self.HEIGHT,
                         highlightthickness=0, **kw)
        self._var = variable or tk.BooleanVar(value=False)
        self._on_change = on_change
        self._var.trace_add("write", lambda *_: self._draw())
        self.bind("<Button-1>", self._toggle)
        self._draw()

    def _toggle(self, _event=None):
        self._var.set(not self._var.get())
        if self._on_change:
            self._on_change(self._var.get())

    def _draw(self):
        self.delete("all")
        on = self._var.get()
        bg = "#34C759" if on else "#AAAAAA"
        # Track
        r = self.HEIGHT // 2
        # Rounded rectangle via arc + line combo (poor man's version)
        self.create_oval(0, 0, self.HEIGHT, self.HEIGHT, fill=bg, outline=bg)
        self.create_oval(self.WIDTH - self.HEIGHT, 0, self.WIDTH, self.HEIGHT, fill=bg, outline=bg)
        self.create_rectangle(r, 0, self.WIDTH - r, self.HEIGHT, fill=bg, outline=bg)
        # Thumb
        pad = 2
        x = (self.WIDTH - self.HEIGHT + pad) if on else pad
        self.create_oval(x, pad, x + self.HEIGHT - 2 * pad,
                         self.HEIGHT - pad, fill="white", outline="white")

    @property
    def value(self) -> bool:
        return self._var.get()

# ═══════════════════════════════════════════
# 4. Autocomplete combobox
# ═══════════════════════════════════════════
class AutocompleteCombobox(ttk.Combobox):
    """Combobox that filters choices as you type."""

    def __init__(self, master, choices: list[str], **kw):
        self._all_choices = choices
        super().__init__(master, values=choices, **kw)
        self.bind("<KeyRelease>", self._on_key)
        self.bind("<FocusIn>",    self._on_focus)

    def _on_focus(self, _event=None):
        self["values"] = self._all_choices

    def _on_key(self, _event=None):
        typed = self.get().lower()
        if not typed:
            self["values"] = self._all_choices
        else:
            filtered = [c for c in self._all_choices if typed in c.lower()]
            self["values"] = filtered
        self.event_generate("<Down>")

# ═══════════════════════════════════════════
# 5. Labeled separator
# ═══════════════════════════════════════════
class LabeledSeparator(tk.Frame):
    """Horizontal separator with a label in the middle."""

    def __init__(self, master, text: str = "", **kw):
        super().__init__(master, **kw)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(2, weight=1)
        ttk.Separator(self, orient="horizontal").grid(row=0, column=0, sticky="ew")
        tk.Label(self, text=f" {text} ", font=("TkDefaultFont", 9), fg="#888").grid(row=0, column=1)
        ttk.Separator(self, orient="horizontal").grid(row=0, column=2, sticky="ew")

# ═══════════════════════════════════════════
# 6. Badge label
# ═══════════════════════════════════════════
class Badge(tk.Label):
    """Colored circular/rounded badge label."""

    def __init__(self, master, text: str = "0",
                 bg: str = "#e74c3c", fg: str = "white", **kw):
        super().__init__(master, text=text, bg=bg, fg=fg,
                         font=("TkDefaultFont", 9, "bold"),
                         padx=5, pady=1, relief="flat", **kw)

    def set(self, value: str | int):
        self.config(text=str(value))

# ═══════════════════════════════════════════
# DEMO
# ═══════════════════════════════════════════
def build_demo():
    root = tk.Tk()
    root.title("Custom Widgets Demo")
    root.geometry("450x520")
    root.resizable(False, False)

    pad = {"padx": 12, "pady": 6}

    # Separator
    LabeledSeparator(root, text="Tooltip").pack(fill="x", **pad)

    btn = tk.Button(root, text="Hover me (tooltip)")
    btn.pack(**pad)
    Tooltip(btn, "This is a tooltip!\nShowing after 500ms delay.")

    # Star rating
    LabeledSeparator(root, text="Star Rating").pack(fill="x", **pad)
    rating_var_frame = tk.Frame(root); rating_var_frame.pack()
    rating_lbl = tk.Label(rating_var_frame, text="Rating: 0 ★")
    rating_lbl.pack(side="right", padx=8)
    def on_rating(v): rating_lbl.config(text=f"Rating: {v} ★")
    StarRating(rating_var_frame, initial=3, on_change=on_rating).pack(side="left")

    # Toggle switch
    LabeledSeparator(root, text="Toggle Switch").pack(fill="x", **pad)
    toggle_frame = tk.Frame(root); toggle_frame.pack()
    toggle_var = tk.BooleanVar(value=True)
    toggle_lbl = tk.Label(toggle_frame, text="Mode: ON")
    toggle_lbl.pack(side="right", padx=8)
    def on_toggle(v): toggle_lbl.config(text=f"Mode: {'ON' if v else 'OFF'}")
    ToggleSwitch(toggle_frame, variable=toggle_var, on_change=on_toggle).pack(side="left")

    # Autocomplete combobox
    LabeledSeparator(root, text="Autocomplete").pack(fill="x", **pad)
    choices = ["Python", "PyPy", "Ruby", "Rust", "R", "Go", "C", "C++", "C#",
               "Java", "JavaScript", "TypeScript", "Kotlin", "Swift", "Scala"]
    ac = AutocompleteCombobox(root, choices, width=30)
    ac.pack(**pad)
    Tooltip(ac, "Start typing to filter languages")

    # Badge demo
    LabeledSeparator(root, text="Badge Labels").pack(fill="x", **pad)
    badges_frame = tk.Frame(root); badges_frame.pack()
    for text, color in [("New", "#27ae60"), ("3", "#e74c3c"), ("Beta", "#2980b9"), ("!", "#e67e22")]:
        Badge(badges_frame, text=text, bg=color).pack(side="left", padx=4)

    # Close button
    tk.Button(root, text="Close", command=root.destroy,
              bg="#e74c3c", fg="white").pack(pady=18)

    root.mainloop()

if __name__ == "__main__":
    build_demo()
