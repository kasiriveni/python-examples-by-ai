# Tkinter GUI example
import tkinter as tk

root = tk.Tk()
root.title('Simple GUI')
label = tk.Label(root, text='Hello Tkinter')
label.pack(padx=20, pady=20)
root.mainloop()
