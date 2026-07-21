#!/usr/bin/env python3
"""Download user-selected found-footage URLs into artifacts/footage.

This script intentionally does not choose clips for the student. Add URLs that you
personally selected to artifacts/selected_sources.txt, one per line, then run:

    python scripts/download_found_footage.py

For Internet Archive item pages, prefer direct downloadable file URLs when possible.
Always verify rights/usage statements before using downloaded footage.
"""
from __future__ import annotations

import sys
import urllib.request
from pathlib import Path
from urllib.parse import unquote, urlparse

ROOT = Path(__file__).resolve().parents[1]
SOURCE_LIST = ROOT / "artifacts" / "selected_sources.txt"
OUT_DIR = ROOT / "artifacts" / "footage"


def filename_for(url: str, index: int) -> str:
    path_name = Path(unquote(urlparse(url).path)).name
    if path_name and "." in path_name:
        return path_name
    return f"source_{index:02d}.download"


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    if not SOURCE_LIST.exists():
        SOURCE_LIST.write_text(
            "# Add user-selected direct media URLs here, one per line.\n",
            encoding="utf-8",
        )
        print(f"Created template: {SOURCE_LIST}")
        return 0

    urls = [
        line.strip()
        for line in SOURCE_LIST.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    ]
    if not urls:
        print(f"No URLs found in {SOURCE_LIST}. Add selected media URLs first.")
        return 0

    for index, url in enumerate(urls, start=1):
        destination = OUT_DIR / filename_for(url, index)
        print(f"Downloading {url} -> {destination}")
        urllib.request.urlretrieve(url, destination)
    return 0


if __name__ == "__main__":
    sys.exit(main())
