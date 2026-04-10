#!/usr/bin/env python3
"""
Start full Fooocus GUI.
Reads version from repositories/Fooocus/fooocus_version.py, clones official
Fooocus repo to repositories/fooocus-full if needed, and starts the full Fooocus UI.
"""

import os
import sys
import subprocess
import re

REPOS_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "repositories"
)
FOOOCUS_VERSION_FILE = os.path.join(REPOS_DIR, "Fooocus", "fooocus_version.py")
FOOOCUS_FULL_DIR = os.path.join(REPOS_DIR, "fooocus-full")
FOOOCUS_REPO_URL = "https://github.com/lllyasviel/Fooocus.git"
FOOOCUS_FULL_PORT = "7865"


def get_fooocus_version():
    """Read version from fooocus_version.py"""
    with open(FOOOCUS_VERSION_FILE, "r") as f:
        content = f.read()
    match = re.search(r"version\s*=\s*['\"](\S+)['\"]", content)
    if not match:
        raise ValueError("Could not find version in fooocus_version.py")
    return match.group(1)


def ensure_fooocus_full_clone(version):
    """Ensure official Fooocus repo is cloned at the matching version tag."""
    if os.path.exists(FOOOCUS_FULL_DIR):
        print(f"fooocus-full already exists at {FOOOCUS_FULL_DIR}, skipping clone.")
        return

    print(f"Cloning Fooocus v{version}...")
    # Clone with depth 1 and specific tag for efficiency
    subprocess.run(
        [
            "git",
            "clone",
            "--depth",
            "1",
            "--branch",
            f"v{version}",
            FOOOCUS_REPO_URL,
            FOOOCUS_FULL_DIR,
        ],
        check=True,
    )
    print(f"Cloned Fooocus v{version} to {FOOOCUS_FULL_DIR}")


def start_fooocus_full():
    """Start full Fooocus web UI server."""
    print(f"Starting Full Fooocus on port {FOOOCUS_FULL_PORT}...")
    conda_env = os.environ.get("CONDA_DEFAULT_ENV", "fooocus-api")
    # Full Fooocus uses python entry_with_update.py with port flag
    subprocess.run(
        [
            "conda",
            "run",
            "-n",
            conda_env,
            "--live-stream",
            "python",
            "entry_with_update.py",
            "--port",
            FOOOCUS_FULL_PORT,
            "--listen"
        ],
        cwd=FOOOCUS_FULL_DIR,
    )


def main():
    version = get_fooocus_version()
    print(f"Fooocus version: {version}")

    ensure_fooocus_full_clone(version)
    start_fooocus_full()

    print(f"\nFull Fooocus running at: http://localhost:{FOOOCUS_FULL_PORT}")


if __name__ == "__main__":
    main()
