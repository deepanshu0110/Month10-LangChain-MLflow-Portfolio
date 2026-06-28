"""
auto_sync_month10.py
====================
Watches:  C:\\Users\\Deepanshu\\OneDrive\\Desktop\\Month10
Repo:     deepanshu0110/Month10-LangChain-MLflow-Portfolio
Branch:   master
Tracks:   .ipynb .py .csv .json .md .txt .png .pdf

Drop any file into the Month10 folder -> auto-commit + push + README update.
Leave this running in a PowerShell / CMD window.

Setup (run once):
    pip install watchdog
    python auto_sync_month10.py
"""

import os
import re
import subprocess
import time
import threading
from datetime import datetime
from pathlib import Path

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

# ── Config ────────────────────────────────────────────────────────────────────
REPO_DIR    = r"C:\Users\Deepanshu\OneDrive\Desktop\Month10"
BRANCH      = "master"
GITHUB_USER = "deepanshu0110"
REPO_NAME   = "Month10-LangChain-MLflow-Portfolio"

TRACKED_EXT = {".ipynb", ".py", ".csv", ".json", ".md", ".txt", ".png", ".pdf"}

DEBOUNCE_SECONDS = 3   # wait 3 s after last change before committing

# Day → topic map  (extend as you progress)
DAY_TOPICS = {
    169: "LangChain Chains & Memory",
    170: "LangChain Tools & Agents",
    171: "Document Loaders + LCEL",
    172: "LangChain Capstone",
    173: "MLflow Experiment Tracking",
    174: "MLflow Model Registry",
    175: "MLflow Capstone",
    176: "Ollama on Colab",
    177: "Evidently Drift Monitoring - Part 1",
    178: "Evidently Drift Monitoring - Part 2",
    179: "Prompt Engineering",
    180: "Month 10 Capstone",
}

# ── Helpers ───────────────────────────────────────────────────────────────────
def extract_day(filename: str) -> int | None:
    """Pull the day number out of a filename like Day173_MLflow_Tracking.ipynb"""
    m = re.search(r"[Dd]ay\s*(\d+)", filename)
    return int(m.group(1)) if m else None


def make_commit_message(filepath: str) -> str:
    name = Path(filepath).name
    day  = extract_day(name)
    if day and day in DAY_TOPICS:
        return f"feat: Day{day} - {DAY_TOPICS[day]} [{name}]"
    elif day:
        return f"feat: Day{day} - {name}"
    else:
        return f"chore: update {name}"


def rebuild_readme(repo_dir: str) -> None:
    """Regenerate README.md with a live file table sorted by day number."""
    files = []
    for ext in TRACKED_EXT:
        for f in Path(repo_dir).glob(f"*{ext}"):
            if f.name in {"README.md", "auto_sync_month10.py"}:
                continue
            day = extract_day(f.name)
            files.append((day or 9999, f.name))

    files.sort()

    rows = []
    for day_num, fname in files:
        topic = DAY_TOPICS.get(day_num, "—")
        ext   = Path(fname).suffix.lstrip(".")
        rows.append(f"| Day {day_num if day_num != 9999 else '—'} | {fname} | {ext.upper()} | {topic} |")

    table = "\n".join(rows) if rows else "| — | No files yet | — | — |"

    readme = f"""# Month 10 — LangChain + MLflow Portfolio

**Student:** Deepanshu Garg | **GitHub:** [{GITHUB_USER}](https://github.com/{GITHUB_USER})  
**Period:** Month 10 of 12-month Data Science & AI Roadmap  
**Last synced:** {datetime.now().strftime('%Y-%m-%d %H:%M')}

---

## Topics Covered

| Week | Days | Focus |
|------|------|-------|
| W1 | 169–172 | LangChain Chains, Agents, LCEL, Capstone |
| W2 | 173–175 | MLflow Experiment Tracking + Model Registry + Capstone |
| W3 | 176–178 | Ollama on Colab + Evidently Drift Monitoring |
| W4 | 179–180 | Prompt Engineering + Month 10 Capstone |

## Tech Stack

`LangChain 0.2.16` · `langchain-groq 0.1.9` · `Groq API (llama-3.1-8b-instant)` ·
`MLflow` · `FAISS` · `Evidently` · `Google Colab T4`

## Dataset

**ReviewPulse India** — 600 freelancer reviews (seed=155)  
Columns: review_id, freelancer_id, review_text, sentiment, rating, hired_again, review_date

---

## Files

| Day | File | Type | Topic |
|-----|------|------|-------|
{table}

---

## Month 10 Scorecard

| Day | Topic | Score |
|-----|-------|-------|
| 169 | LangChain Chains & Memory | ✅ 80/80+10★ |
| 170 | LangChain Tools & Agents | ✅ 80/80+10★ |
| 171 | Document Loaders + LCEL | ✅ 80/80+10★ |
| 172 | LangChain Capstone | ✅ 90/90+10★ |

*Table updates automatically via auto_sync_month10.py*
"""

    readme_path = os.path.join(repo_dir, "README.md")
    with open(readme_path, "w", encoding="utf-8") as fh:
        fh.write(readme)


def git(args: list[str], cwd: str) -> None:
    subprocess.run(["git"] + args, cwd=cwd, check=True)


def commit_and_push(changed_files: list[str]) -> None:
    """Stage changed files, rebuild README, commit, push."""
    try:
        # Stage changed files
        for f in changed_files:
            git(["add", f], REPO_DIR)

        # Rebuild + stage README
        rebuild_readme(REPO_DIR)
        git(["add", "README.md"], REPO_DIR)

        # Build commit message
        if len(changed_files) == 1:
            msg = make_commit_message(changed_files[0])
        else:
            days = sorted({extract_day(f) for f in changed_files if extract_day(f)})
            day_str = "/".join(f"Day{d}" for d in days) if days else "batch"
            msg = f"feat: {day_str} - {len(changed_files)} files updated"

        git(["commit", "-m", msg], REPO_DIR)
        git(["push", "origin", BRANCH], REPO_DIR)

        print(f"[{datetime.now().strftime('%H:%M:%S')}] ✅ Pushed — {msg}")

    except subprocess.CalledProcessError as e:
        print(f"[{datetime.now().strftime('%H:%M:%S')}] ❌ Git error: {e}")


# ── Watchdog handler ──────────────────────────────────────────────────────────
class SyncHandler(FileSystemEventHandler):
    def __init__(self):
        self._pending: dict[str, float] = {}
        self._lock    = threading.Lock()
        self._timer: threading.Timer | None = None

    def _schedule_flush(self) -> None:
        if self._timer and self._timer.is_alive():
            self._timer.cancel()
        self._timer = threading.Timer(DEBOUNCE_SECONDS, self._flush)
        self._timer.start()

    def _flush(self) -> None:
        with self._lock:
            files = list(self._pending.keys())
            self._pending.clear()
        if files:
            commit_and_push(files)

    def on_modified(self, event):
        self._handle(event)

    def on_created(self, event):
        self._handle(event)

    def _handle(self, event) -> None:
        if event.is_directory:
            return
        path = event.src_path
        ext  = Path(path).suffix.lower()
        name = Path(path).name

        if ext not in TRACKED_EXT:
            return
        if name.startswith(".") or name == "README.md":
            return
        if "auto_sync" in name.lower():
            return

        rel = os.path.relpath(path, REPO_DIR)
        with self._lock:
            self._pending[rel] = time.time()

        print(f"[{datetime.now().strftime('%H:%M:%S')}] 📝 Detected: {name}")
        self._schedule_flush()


# ── Entry point ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    if not os.path.isdir(REPO_DIR):
        print(f"❌ Folder not found: {REPO_DIR}")
        print("   Create it first:  mkdir \"" + REPO_DIR + "\"")
        raise SystemExit(1)

    print("=" * 60)
    print(f"  Month 10 Auto-Sync — {REPO_NAME}")
    print(f"  Watching : {REPO_DIR}")
    print(f"  Branch   : {BRANCH}")
    print(f"  Debounce : {DEBOUNCE_SECONDS}s")
    print(f"  Tracks   : {' '.join(sorted(TRACKED_EXT))}")
    print("=" * 60)
    print("  Drop any file into the folder → auto-commit + push")
    print("  Press Ctrl+C to stop.")
    print("=" * 60)

    handler  = SyncHandler()
    observer = Observer()
    observer.schedule(handler, REPO_DIR, recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        print("\n[auto_sync] Stopped.")

    observer.join()
