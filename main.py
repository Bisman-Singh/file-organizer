#!/usr/bin/env python3
"""Automatically organize files in a directory by sorting them into categorized folders."""

import os
import sys
import shutil
import argparse
import time
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

CATEGORIES = {
    "Images": {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp", ".ico", ".tiff"},
    "Documents": {".pdf", ".doc", ".docx", ".txt", ".rtf", ".odt", ".xls", ".xlsx", ".ppt", ".pptx", ".csv"},
    "Videos": {".mp4", ".avi", ".mkv", ".mov", ".wmv", ".flv", ".webm"},
    "Audio": {".mp3", ".wav", ".flac", ".aac", ".ogg", ".wma", ".m4a"},
    "Archives": {".zip", ".rar", ".7z", ".tar", ".gz", ".bz2", ".xz"},
    "Code": {".py", ".js", ".ts", ".html", ".css", ".java", ".cpp", ".c", ".go", ".rs", ".rb", ".php", ".sh"},
    "Data": {".json", ".xml", ".yaml", ".yml", ".sql", ".db", ".sqlite"},
    "Executables": {".exe", ".msi", ".dmg", ".app", ".deb", ".rpm"},
    "Fonts": {".ttf", ".otf", ".woff", ".woff2"},
}


def get_category(extension: str) -> str:
    ext = extension.lower()
    for category, extensions in CATEGORIES.items():
        if ext in extensions:
            return category
    return "Other"


def organize_file(filepath: Path, target_dir: Path, dry_run: bool = False):
    if filepath.name.startswith(".") or filepath.is_dir():
        return

    category = get_category(filepath.suffix)
    dest_folder = target_dir / category
    dest_path = dest_folder / filepath.name

    if dest_path.exists():
        stem = filepath.stem
        suffix = filepath.suffix
        counter = 1
        while dest_path.exists():
            dest_path = dest_folder / f"{stem}_{counter}{suffix}"
            counter += 1

    if dry_run:
        print(f"  [DRY RUN] {filepath.name} -> {category}/")
    else:
        dest_folder.mkdir(exist_ok=True)
        shutil.move(str(filepath), str(dest_path))
        print(f"  Moved: {filepath.name} -> {category}/")


def organize_directory(directory: Path, dry_run: bool = False):
    files = [f for f in directory.iterdir() if f.is_file() and not f.name.startswith(".")]
    if not files:
        print("No files to organize.")
        return

    print(f"Found {len(files)} file(s) to organize.\n")
    for filepath in sorted(files):
        organize_file(filepath, directory, dry_run)
    print(f"\nDone! Organized {len(files)} files.")


class FileHandler(FileSystemEventHandler):
    def __init__(self, target_dir: Path):
        self.target_dir = target_dir

    def on_created(self, event):
        if not event.is_directory:
            filepath = Path(event.src_path)
            time.sleep(0.5)  # wait for file write to complete
            if filepath.exists():
                organize_file(filepath, self.target_dir)


def watch_directory(directory: Path):
    print(f"Watching '{directory}' for new files... (Ctrl+C to stop)\n")
    handler = FileHandler(directory)
    observer = Observer()
    observer.schedule(handler, str(directory), recursive=False)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        print("\nStopped watching.")
    observer.join()


def show_summary(directory: Path):
    print("\nCategory Summary:")
    print("-" * 40)
    for category in sorted(CATEGORIES.keys()):
        cat_dir = directory / category
        if cat_dir.exists():
            count = len(list(cat_dir.iterdir()))
            print(f"  {category:15s} : {count} file(s)")
    other_dir = directory / "Other"
    if other_dir.exists():
        count = len(list(other_dir.iterdir()))
        print(f"  {'Other':15s} : {count} file(s)")


def main():
    parser = argparse.ArgumentParser(description="Organize files in a directory by type")
    parser.add_argument("directory", nargs="?", default=".", help="Directory to organize (default: current)")
    parser.add_argument("--watch", "-w", action="store_true", help="Watch directory for new files")
    parser.add_argument("--dry-run", "-d", action="store_true", help="Preview without moving files")
    parser.add_argument("--summary", "-s", action="store_true", help="Show category summary")
    args = parser.parse_args()

    directory = Path(args.directory).resolve()
    if not directory.is_dir():
        print(f"Error: '{directory}' is not a valid directory.")
        sys.exit(1)

    if args.summary:
        show_summary(directory)
    elif args.watch:
        watch_directory(directory)
    else:
        organize_directory(directory, dry_run=args.dry_run)


if __name__ == "__main__":
    main()
