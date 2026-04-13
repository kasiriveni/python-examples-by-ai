"""
GUI Development: Background threading in Tkinter (thread-safe GUI updates).
"""
import tkinter as tk
from tkinter import ttk
import threading
import queue
import time
import random
import itertools

# ═══════════════════════════════════════════
# Thread-safe message queue pattern
# ═══════════════════════════════════════════
class ThreadedApp(tk.Tk):
    """
    Tkinter is NOT thread-safe — never update widgets from a worker thread.
    Safe pattern: worker puts messages on a Queue, main thread polls with after().
    """

    def __init__(self):
        super().__init__()
        self.title("Threading in Tkinter")
        self.geometry("700x550")
        self._queue: queue.Queue = queue.Queue()
        self._tasks: dict[int, threading.Thread] = {}
        self._counter = itertools.count(1)
        self._build_ui()
        self._poll()          # start queue polling loop

    def _build_ui(self):
        # Controls
        ctrl = ttk.Frame(self, padding=8)
        ctrl.pack(fill=tk.X)

        ttk.Button(ctrl, text="Download (slow)", command=self._start_download).pack(side=tk.LEFT, padx=3)
        ttk.Button(ctrl, text="Fibonacci heavy", command=self._start_fibonacci).pack(side=tk.LEFT, padx=3)
        ttk.Button(ctrl, text="Progress bar",    command=self._start_progress).pack(side=tk.LEFT, padx=3)
        ttk.Button(ctrl, text="Cancel all",      command=self._cancel_all).pack(side=tk.RIGHT, padx=3)

        # Progress area
        bar_frame = ttk.LabelFrame(self, text="Tasks", padding=4)
        bar_frame.pack(fill=tk.X, padx=8, pady=4)
        self._bars: dict[int, ttk.Progressbar] = {}
        self._bar_labels: dict[int, ttk.Label] = {}
        self._bar_frame = bar_frame

        # Log
        log_frame = ttk.LabelFrame(self, text="Log", padding=4)
        log_frame.pack(fill=tk.BOTH, expand=True, padx=8, pady=4)

        self._log = tk.Text(log_frame, height=10, state=tk.DISABLED, font=("Courier", 10))
        sb = ttk.Scrollbar(log_frame, command=self._log.yview)
        self._log.config(yscrollcommand=sb.set)
        sb.pack(side=tk.RIGHT, fill=tk.Y)
        self._log.pack(fill=tk.BOTH, expand=True)

        # Status bar
        self._status = tk.StringVar(value="Ready")
        ttk.Label(self, textvariable=self._status, relief=tk.SUNKEN,
                  anchor=tk.W, padding=2).pack(fill=tk.X, side=tk.BOTTOM)

    # ─────────────────────────────────────
    def _log_msg(self, msg: str):
        self._log.config(state=tk.NORMAL)
        self._log.insert(tk.END, msg + "\n")
        self._log.see(tk.END)
        self._log.config(state=tk.DISABLED)

    def _poll(self):
        """Drain the message queue and update GUI. Called every 50ms."""
        try:
            while True:
                msg = self._queue.get_nowait()
                self._handle_message(msg)
        except queue.Empty:
            pass
        self.after(50, self._poll)

    def _handle_message(self, msg: dict):
        kind = msg.get("kind")
        task_id = msg.get("id")

        if kind == "log":
            self._log_msg(f"[Task-{task_id}] {msg['text']}")

        elif kind == "progress":
            if task_id in self._bars:
                self._bars[task_id]["value"] = msg["value"]
                self._bar_labels[task_id].configure(
                    text=f"Task-{task_id}: {msg['label']}"
                )

        elif kind == "done":
            self._log_msg(f"[Task-{task_id}] ✓ {msg.get('result', 'done')}")
            if task_id in self._bars:
                self._bars[task_id]["value"] = 100
                self._bar_labels[task_id].configure(text=f"Task-{task_id}: Done ✓")
            self._tasks.pop(task_id, None)
            self._status.set(f"{len(self._tasks)} tasks running")

        elif kind == "error":
            self._log_msg(f"[Task-{task_id}] ERROR: {msg['error']}")
            self._tasks.pop(task_id, None)

    def _add_progress_row(self, task_id: int, label: str):
        row = ttk.Frame(self._bar_frame)
        row.pack(fill=tk.X, pady=1)
        lbl = ttk.Label(row, text=f"Task-{task_id}: {label}", width=30, anchor=tk.W)
        lbl.pack(side=tk.LEFT)
        bar = ttk.Progressbar(row, mode="determinate", maximum=100)
        bar.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self._bars[task_id] = bar
        self._bar_labels[task_id] = lbl

    # ─────────────────────────────────────
    def _run_task(self, task_id: int, fn, *args):
        """Run fn(*args) in a thread; fn should post to self._queue."""
        t = threading.Thread(target=fn, args=(task_id, *args), daemon=True)
        self._tasks[task_id] = t
        t.start()
        self._status.set(f"{len(self._tasks)} tasks running")

    def _start_download(self):
        task_id = next(self._counter)
        self._add_progress_row(task_id, "Downloading…")
        self._run_task(task_id, self._fake_download)

    def _fake_download(self, task_id: int):
        chunks = random.randint(5, 15)
        total_size = random.choice([512, 1024, 2048])
        downloaded = 0
        for i in range(chunks):
            time.sleep(random.uniform(0.1, 0.4))
            downloaded += total_size // chunks
            pct = min(100, int(downloaded / total_size * 100))
            self._queue.put({"kind": "progress", "id": task_id,
                             "value": pct, "label": f"{downloaded}/{total_size} KB"})
        self._queue.put({"kind": "done", "id": task_id,
                         "result": f"Downloaded {total_size} KB"})

    def _start_fibonacci(self):
        task_id = next(self._counter)
        n = random.randint(30, 35)
        self._add_progress_row(task_id, f"Fibonacci({n})…")
        self._run_task(task_id, self._heavy_fibonacci, n)

    def _heavy_fibonacci(self, task_id: int, n: int):
        self._queue.put({"kind": "log", "id": task_id, "text": f"Computing fib({n})…"})
        def fib(n):
            if n <= 1: return n
            return fib(n-1) + fib(n-2)
        try:
            start = time.perf_counter()
            result = fib(n)
            elapsed = time.perf_counter() - start
            self._queue.put({"kind": "progress", "id": task_id, "value": 100, "label": "Done"})
            self._queue.put({"kind": "done", "id": task_id,
                             "result": f"fib({n})={result} in {elapsed:.2f}s"})
        except Exception as e:
            self._queue.put({"kind": "error", "id": task_id, "error": str(e)})

    def _start_progress(self):
        task_id = next(self._counter)
        self._add_progress_row(task_id, "Processing…")
        self._run_task(task_id, self._progress_task)

    def _progress_task(self, task_id: int):
        steps = random.randint(10, 20)
        for i in range(steps):
            time.sleep(random.uniform(0.05, 0.2))
            pct = int((i+1) / steps * 100)
            self._queue.put({"kind": "progress", "id": task_id,
                             "value": pct, "label": f"Step {i+1}/{steps}"})
        self._queue.put({"kind": "done", "id": task_id, "result": f"Processed {steps} steps"})

    def _cancel_all(self):
        # Daemon threads will exit when the app closes.
        # In a real app you'd use threading.Event to signal cancellation.
        self._log_msg("Cancel requested — daemon threads will stop when app exits.")
        self._tasks.clear()
        self._status.set("Cancelled")

if __name__ == "__main__":
    print("Launch threading GUI demo (close window to exit)...")
    ThreadedApp().mainloop()
