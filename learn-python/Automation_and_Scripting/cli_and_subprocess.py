"""
Automation and Scripting: CLI tools, subprocess, cron-style scheduling, file watching.
"""
from __future__ import annotations
import argparse
import subprocess
import shutil
import sys
import os
import time
import threading
import hashlib
import stat
from pathlib import Path
from dataclasses import dataclass, field
from typing import Callable

# ═══════════════════════════════════════════
# 1. argparse — CLI argument parsing
# ═══════════════════════════════════════════
def build_cli_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="deploy",
        description="Deployment automation tool",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("environment",
                        choices=["dev", "staging", "prod"],
                        help="Target deployment environment")
    parser.add_argument("--version", "-v",
                        required=True,
                        help="Version tag to deploy (e.g. v1.2.3)")
    parser.add_argument("--dry-run",
                        action="store_true",
                        help="Print actions without executing them")
    parser.add_argument("--service",
                        nargs="+",
                        default=["app", "worker"],
                        help="Services to deploy (space-separated)")
    parser.add_argument("--timeout",
                        type=int,
                        default=300,
                        metavar="SECONDS",
                        help="Deployment timeout")
    parser.add_argument("--config",
                        type=Path,
                        default=Path("deploy.toml"),
                        help="Config file path")
    parser.add_argument("--log-level",
                        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
                        default="INFO",
                        help="Logging verbosity")
    return parser

def build_subcommand_parser() -> argparse.ArgumentParser:
    """Demonstrate sub-commands (git-style CLI)."""
    parser = argparse.ArgumentParser(prog="ctl")
    sub = parser.add_subparsers(dest="command", metavar="COMMAND")

    # ctl start [--port PORT]
    start = sub.add_parser("start", help="Start the service")
    start.add_argument("--port", type=int, default=8080)

    # ctl stop [--force]
    stop = sub.add_parser("stop", help="Stop the service")
    stop.add_argument("--force", action="store_true")

    # ctl status
    sub.add_parser("status", help="Show service status")

    return parser

# ═══════════════════════════════════════════
# 2. subprocess patterns
# ═══════════════════════════════════════════
def run_command(cmd: list[str],
                cwd: Path | None = None,
                env: dict | None = None,
                timeout: int = 60,
                capture: bool = True) -> tuple[int, str, str]:
    """Run a command; returns (returncode, stdout, stderr)."""
    result = subprocess.run(
        cmd,
        cwd=cwd,
        env={**os.environ, **(env or {})},
        capture_output=capture,
        text=True,
        timeout=timeout,
    )
    return result.returncode, result.stdout.strip(), result.stderr.strip()

def run_pipeline(commands: list[list[str]]) -> str:
    """Pipe stdout of each command into the next."""
    procs = []
    for i, cmd in enumerate(commands):
        stdin = procs[-1].stdout if procs else None
        p = subprocess.Popen(cmd, stdin=stdin,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE,
                             text=True)
        procs.append(p)

    # Close intermediate stdouts
    for p in procs[:-1]:
        p.stdout.close()

    stdout, stderr = procs[-1].communicate()
    for p in procs[:-1]:
        p.wait()

    return stdout.strip()

def git_info(repo_path: Path) -> dict[str, str]:
    """Extract git metadata from a repository."""
    info: dict[str, str] = {}
    cmds = {
        "branch":  ["git", "rev-parse", "--abbrev-ref", "HEAD"],
        "commit":  ["git", "rev-parse", "--short", "HEAD"],
        "message": ["git", "log", "-1", "--pretty=%s"],
        "author":  ["git", "log", "-1", "--pretty=%an"],
        "status":  ["git", "status", "--porcelain"],
    }
    for key, cmd in cmds.items():
        rc, out, _ = run_command(cmd, cwd=repo_path)
        info[key] = out if rc == 0 else "N/A"
    return info

# ═══════════════════════════════════════════
# 3. File system automation
# ═══════════════════════════════════════════
def find_large_files(root: Path, min_mb: float = 1.0) -> list[tuple[Path, float]]:
    """Find files larger than min_mb megabytes."""
    min_bytes = int(min_mb * 1024 * 1024)
    results = []
    for p in root.rglob("*"):
        if p.is_file():
            try:
                size = p.stat().st_size
                if size >= min_bytes:
                    results.append((p, size / 1024 / 1024))
            except (OSError, PermissionError):
                pass
    return sorted(results, key=lambda t: t[1], reverse=True)

def create_dated_backup(src: Path, backup_dir: Path) -> Path:
    """Copy a dir/file to backup_dir/<name>_YYYYMMDD_HHMMSS."""
    ts = time.strftime("%Y%m%d_%H%M%S")
    dest = backup_dir / f"{src.name}_{ts}"
    backup_dir.mkdir(parents=True, exist_ok=True)
    if src.is_dir():
        shutil.copytree(src, dest)
    else:
        shutil.copy2(src, dest)
    return dest

def set_executable(path: Path) -> None:
    """Mark a file as executable (chmod +x equivalent)."""
    current = stat.S_IMODE(path.stat().st_mode)
    path.chmod(current | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)

# ═══════════════════════════════════════════
# 4. Simple scheduler (cron-style)
# ═══════════════════════════════════════════
@dataclass
class Job:
    name: str
    fn: Callable
    interval_seconds: float
    last_run: float = field(default_factory=lambda: 0.0)

    def is_due(self, now: float) -> bool:
        return (now - self.last_run) >= self.interval_seconds

class Scheduler:
    """Simple in-process task scheduler (not production — use APScheduler for that)."""

    def __init__(self):
        self._jobs: list[Job] = []
        self._running = False
        self._thread: threading.Thread | None = None

    def add_job(self, name: str, fn: Callable, interval_seconds: float):
        self._jobs.append(Job(name=name, fn=fn, interval_seconds=interval_seconds))
        return self

    def _loop(self):
        while self._running:
            now = time.time()
            for job in self._jobs:
                if job.is_due(now):
                    try:
                        job.fn()
                    except Exception as e:
                        print(f"  [Scheduler] Job {job.name!r} failed: {e}")
                    job.last_run = now
            time.sleep(0.1)

    def start(self):
        self._running = True
        self._thread = threading.Thread(target=self._loop, daemon=True)
        self._thread.start()

    def stop(self):
        self._running = False

# ═══════════════════════════════════════════
# 5. File watcher (polling-based)
# ═══════════════════════════════════════════
class FileWatcher:
    """Watch a directory for changes (polling). For production use watchdog."""

    WatchEvent = tuple[str, Path]  # ("created"|"modified"|"deleted", path)

    def __init__(self, directory: Path, poll_interval: float = 0.5):
        self.directory = directory
        self.poll_interval = poll_interval
        self._snapshot: dict[Path, tuple[float, int]] = {}
        self._callbacks: list[Callable[[str, Path], None]] = []
        self._thread: threading.Thread | None = None
        self._running = False

    def on_change(self, fn: Callable[[str, Path], None]):
        self._callbacks.append(fn); return self

    def _get_snapshot(self) -> dict[Path, tuple[float, int]]:
        snap: dict[Path, tuple[float, int]] = {}
        for p in self.directory.rglob("*"):
            if p.is_file():
                try:
                    s = p.stat()
                    snap[p] = (s.st_mtime, s.st_size)
                except OSError:
                    pass
        return snap

    def _emit(self, event: str, path: Path):
        for cb in self._callbacks:
            cb(event, path)

    def _poll(self):
        self._snapshot = self._get_snapshot()
        while self._running:
            time.sleep(self.poll_interval)
            new_snap = self._get_snapshot()
            for p, info in new_snap.items():
                if p not in self._snapshot:
                    self._emit("created", p)
                elif info != self._snapshot[p]:
                    self._emit("modified", p)
            for p in self._snapshot:
                if p not in new_snap:
                    self._emit("deleted", p)
            self._snapshot = new_snap

    def start(self):
        self._running = True
        self._thread = threading.Thread(target=self._poll, daemon=True)
        self._thread.start()
        return self

    def stop(self): self._running = False

# ═══════════════════════════════════════════
# DEMO
# ═══════════════════════════════════════════
if __name__ == "__main__":
    print("=== argparse CLI ===")
    parser = build_cli_parser()
    args = parser.parse_args(["prod", "--version", "v2.1.0",
                              "--dry-run", "--service", "app", "worker"])
    print(f"  env={args.environment}, version={args.version}, "
          f"dry_run={args.dry_run}, services={args.service}")

    print("\n=== subcommand CLI ===")
    sub_parser = build_subcommand_parser()
    for raw in [["start", "--port", "9090"], ["stop", "--force"], ["status"]]:
        ns = sub_parser.parse_args(raw)
        print(f"  {raw} → {vars(ns)}")

    print("\n=== subprocess ===")
    if sys.platform == "win32":
        rc, out, err = run_command(["python", "--version"])
    else:
        rc, out, err = run_command(["python3", "--version"])
    print(f"  returncode={rc}  output={out!r}")

    print("\n=== File system automation ===")
    import tempfile
    with tempfile.TemporaryDirectory() as tmpdir:
        base = Path(tmpdir)
        # Create sample files
        for i in range(3):
            (base / f"file_{i}.txt").write_text(f"Content {i}" * 100)
        large = find_large_files(base, min_mb=0.0)
        print(f"  Found {len(large)} files")
        for p, mb in large:
            print(f"    {p.name}: {mb*1024:.1f} KB")

    print("\n=== Scheduler demo (1 second) ===")
    tick_count = [0]
    sched = Scheduler()
    sched.add_job("ticker", lambda: tick_count.__setitem__(0, tick_count[0] + 1), 0.2)
    sched.start()
    time.sleep(1.1)
    sched.stop()
    print(f"  Ticked {tick_count[0]} times in ~1s (expected ~5)")

    print("\n=== File watcher demo ===")
    events: list[tuple[str, str]] = []
    with tempfile.TemporaryDirectory() as wd:
        watcher = FileWatcher(Path(wd), poll_interval=0.1)
        watcher.on_change(lambda evt, p: events.append((evt, p.name)))
        watcher.start()
        time.sleep(0.15)
        (Path(wd) / "test.txt").write_text("hello")
        time.sleep(0.25)
        (Path(wd) / "test.txt").write_text("changed")
        time.sleep(0.25)
        (Path(wd) / "test.txt").unlink()
        time.sleep(0.25)
        watcher.stop()
    print(f"  Events: {events}")
