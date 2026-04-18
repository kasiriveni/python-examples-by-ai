# Core Python Concepts

## Core Themes
- Tkinter widgets, layouts, and event-driven programming.
- Dialogs, menus, tables, drawing, and reusable widget design.
- Thread-safe GUI updates and background-task coordination.

## Core Theme Examples
- Example 1: Building layout hierarchies with pack and grid.
- Example 2: Creating file dialogs and custom message boxes.
- Example 3: Queuing background worker tasks to prevent UI freezing.

## Files and Concepts
- canvas_drawing.py: Canvas drawing primitives, scrollbars, event binding
- custom_widgets.py: tooltip components, hover events, reusable widget classes
- data_table.py: Treeview tables, sorting, editing, CSV export
- dialogs_and_menus.py: menu bars, message boxes, file dialogs, color chooser
- threading_in_gui.py: queues, worker threads, progress bars, UI thread safety
- tkinter_basics.py: windows, labels, buttons, simple callbacks
- tkinter_example.py: basic widget setup and mainloop structure
- widget_layouts.py: pack, grid, place, frame hierarchies

## Core Example
This example creates a tiny Tkinter window with a label and button.

```python
import tkinter as tk

root = tk.Tk()
root.title("Demo")
tk.Label(root, text="Hello").pack()
tk.Button(root, text="Close", command=root.destroy).pack()

# root.mainloop()
print(root.title())
root.destroy()
```
