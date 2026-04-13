"""
GUI Development: Canvas drawing and custom widgets in Tkinter.
"""
import tkinter as tk
from tkinter import ttk
import math
import time

# ═══════════════════════════════════════════
# 1. Canvas drawing primitives
# ═══════════════════════════════════════════
class DrawingApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Canvas Drawing")
        self.geometry("700x550")
        self._setup()

    def _setup(self):
        # Toolbar
        bar = ttk.Frame(self)
        bar.pack(fill=tk.X)
        for text, cmd in [
            ("Lines",     self.draw_lines),
            ("Shapes",    self.draw_shapes),
            ("Text",      self.draw_text),
            ("Clock",     self.draw_clock),
            ("Bezier",    self.draw_bezier),
            ("Clear",     self.clear),
        ]:
            ttk.Button(bar, text=text, command=cmd, width=8).pack(side=tk.LEFT, padx=2, pady=2)

        # Canvas with scrollbars
        frame = ttk.Frame(self)
        frame.pack(fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(frame, bg="white", cursor="crosshair")
        hbar = ttk.Scrollbar(frame, orient=tk.HORIZONTAL, command=self.canvas.xview)
        vbar = ttk.Scrollbar(frame, orient=tk.VERTICAL,   command=self.canvas.yview)
        self.canvas.config(xscrollcommand=hbar.set, yscrollcommand=vbar.set,
                           scrollregion=(0, 0, 1200, 900))

        vbar.pack(side=tk.RIGHT, fill=tk.Y)
        hbar.pack(side=tk.BOTTOM, fill=tk.X)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Mouse events
        self.canvas.bind("<B1-Motion>", self._freehand)
        self.canvas.bind("<ButtonRelease-1>", lambda e: setattr(self, "_prev", None))
        self._prev = None

        self._clock_job = None
        self.draw_shapes()

    def clear(self):
        self.canvas.delete("all")
        if self._clock_job:
            self.after_cancel(self._clock_job)
            self._clock_job = None

    def draw_lines(self):
        self.clear()
        c = self.canvas
        # Dashed line
        c.create_line(20, 20, 300, 20, fill="blue", width=2, dash=(8, 4))
        # Arrow
        c.create_line(20, 60, 300, 60, fill="red", arrow=tk.LAST, width=2)
        # Smooth spline
        points = [20, 100, 100, 50, 200, 150, 300, 80, 400, 120]
        c.create_line(points, smooth=True, fill="green", width=3)
        # Polygon outline
        coords = [50, 200, 150, 180, 200, 250, 120, 300, 30, 260]
        c.create_polygon(coords, fill="", outline="purple", width=2)

    def draw_shapes(self):
        self.clear()
        c = self.canvas
        # Rectangle
        c.create_rectangle(20, 20, 150, 100, fill="#3498db", outline="navy", width=2)
        c.create_text(85, 60, text="Rectangle", fill="white", font=("Arial", 10, "bold"))
        # Oval
        c.create_oval(170, 20, 320, 100, fill="#e74c3c", outline="darkred")
        c.create_text(245, 60, text="Oval", fill="white", font=("Arial", 10, "bold"))
        # Arc
        c.create_arc(340, 20, 490, 120, start=30, extent=270, fill="#2ecc71", style=tk.PIESLICE)
        # Polygon (star)
        cx, cy, n, r1, r2 = 570, 80, 5, 55, 25
        points = []
        for i in range(n * 2):
            angle = math.pi * i / n - math.pi / 2
            r = r1 if i % 2 == 0 else r2
            points.extend([cx + r * math.cos(angle), cy + r * math.sin(angle)])
        c.create_polygon(points, fill="#f39c12", outline="#e67e22", width=2)
        # Gradient-like effect using overlapping rectangles
        for i, color in enumerate(["#ecf0f1","#bdc3c7","#95a5a6","#7f8c8d","#636e72","#2d3436"]):
            c.create_rectangle(20 + i*20, 160, 40 + i*20, 230, fill=color, outline="")

    def draw_text(self):
        self.clear()
        c = self.canvas
        for i, (size, weight) in enumerate([(8, "normal"), (10, "normal"), (12, "bold"),
                                             (14, "bold"), (18, "bold italic"), (24, "bold")]):
            c.create_text(20, 20 + i*35, text=f"Font size={size} weight={weight}",
                          font=("Arial", size, weight), anchor=tk.W)
        # Rotated text
        for angle in range(0, 360, 45):
            rad = math.radians(angle)
            x = 400 + 100 * math.cos(rad)
            y = 300 + 100 * math.sin(rad)
            c.create_text(x, y, text=f"{angle}°", font=("Arial", 9))

    def draw_clock(self):
        self.clear()
        self._update_clock()

    def _update_clock(self):
        self.canvas.delete("clock")
        c = self.canvas
        cx, cy, r = 300, 250, 180
        # Face
        c.create_oval(cx-r, cy-r, cx+r, cy+r, fill="#2c3e50", outline="#ecf0f1",
                      width=4, tags="clock")
        # Hour marks
        for i in range(12):
            angle = math.radians(i * 30 - 90)
            r1 = r - 20 if i % 3 == 0 else r - 10
            x1 = cx + r1 * math.cos(angle)
            y1 = cy + r1 * math.sin(angle)
            x2 = cx + (r-5) * math.cos(angle)
            y2 = cy + (r-5) * math.sin(angle)
            c.create_line(x1, y1, x2, y2, fill="white", width=3 if i%3==0 else 1, tags="clock")

        now = time.localtime()
        # Hour hand
        ha = math.radians((now.tm_hour % 12 + now.tm_min/60) * 30 - 90)
        c.create_line(cx, cy, cx + 80*math.cos(ha), cy + 80*math.sin(ha),
                      fill="#ecf0f1", width=6, capstyle=tk.ROUND, tags="clock")
        # Minute hand
        ma = math.radians(now.tm_min * 6 - 90)
        c.create_line(cx, cy, cx + 120*math.cos(ma), cy + 120*math.sin(ma),
                      fill="#3498db", width=4, capstyle=tk.ROUND, tags="clock")
        # Second hand
        sa = math.radians(now.tm_sec * 6 - 90)
        c.create_line(cx, cy, cx + 140*math.cos(sa), cy + 140*math.sin(sa),
                      fill="#e74c3c", width=2, tags="clock")
        c.create_oval(cx-6, cy-6, cx+6, cy+6, fill="white", tags="clock")

        self._clock_job = self.after(1000, self._update_clock)

    def draw_bezier(self):
        self.clear()
        c = self.canvas
        # Approximate cubic Bézier using many line segments
        def bezier(p0, p1, p2, p3, steps=60):
            pts = []
            for i in range(steps + 1):
                t = i / steps
                x = ((1-t)**3*p0[0] + 3*(1-t)**2*t*p1[0] +
                     3*(1-t)*t**2*p2[0] + t**3*p3[0])
                y = ((1-t)**3*p0[1] + 3*(1-t)**2*t*p1[1] +
                     3*(1-t)*t**2*p2[1] + t**3*p3[1])
                pts.extend([x, y])
            return pts

        curves = [
            ((50,300), (100,50),  (500,50),  (550,300)),
            ((50,300), (200,500), (350,100), (550,300)),
            ((100,150),(200,400), (400,50),  (600,200)),
        ]
        colors = ["#e74c3c", "#3498db", "#2ecc71"]
        for (p0,p1,p2,p3), color in zip(curves, colors):
            pts = bezier(p0, p1, p2, p3)
            c.create_line(pts, fill=color, width=3, smooth=False)
            for pt in [p0, p1, p2, p3]:
                c.create_oval(pt[0]-4, pt[1]-4, pt[0]+4, pt[1]+4, fill=color)

    def _freehand(self, event):
        if self._prev:
            self.canvas.create_line(self._prev[0], self._prev[1],
                                     event.x, event.y,
                                     fill="black", width=2, capstyle=tk.ROUND)
        self._prev = (event.x, event.y)

if __name__ == "__main__":
    print("Launch canvas drawing app (close window to exit)...")
    app = DrawingApp()
    app.mainloop()
