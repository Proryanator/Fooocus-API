#!/usr/bin/env python3
"""
Clone and run full Fooocus alongside Fooocus API.
Reads version from repositories/Fooocus/fooocus_version.py, clones official
Fooocus repo to repositories/fooocus-full, and starts both servers.
"""

import os
import sys
import subprocess
import shutil
import re

REPOS_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "repositories"
)
FOOOCUS_API_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FOOOCUS_VERSION_FILE = os.path.join(REPOS_DIR, "Fooocus", "fooocus_version.py")
FOOOCUS_FULL_DIR = os.path.join(REPOS_DIR, "fooocus-full")
FOOOCUS_REPO_URL = "https://github.com/lllyasviel/Fooocus.git"
FOOOCUS_API_PORT = "8888"
FOOOCUS_FULL_PORT = "7865"


def get_fooocus_version():
    """Read version from fooocus_version.py"""
    with open(FOOOCUS_VERSION_FILE, "r") as f:
        content = f.read()
    match = re.search(r"version\s*=\s*['\"](\S+)['\"]", content)
    if not match:
        raise ValueError("Could not find version in fooocus_version.py")
    return match.group(1)


def clone_fooocus_full(version):
    """Clone official Fooocus repo at the matching version tag."""
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


def start_fooocus_api():
    """Start Fooocus API server."""
    print("Starting Fooocus API on port 8888...")
    conda_env = os.environ.get("CONDA_DEFAULT_ENV", "fooocus-api")
    subprocess.Popen(
        [
            "conda",
            "run",
            "-n",
            conda_env,
            "--live-stream",
            "python",
            "main.py",
            "--host",
            "0.0.0.0",
        ],
        cwd=FOOOCUS_API_DIR,
    )


def start_fooocus_full():
    """Start full Fooocus web UI server."""
    print("Starting Full Fooocus on port 7865...")
    conda_env = os.environ.get("CONDA_DEFAULT_ENV", "fooocus-api")
    # Full Fooocus uses python entrypoint.py with port flag
    subprocess.Popen(
        [
            "conda",
            "run",
            "-n",
            conda_env,
            "--live-stream",
            "python",
            "entrypoint.py",
            "--port",
            FOOOCUS_FULL_PORT,
            "--host",
            "0.0.0.0",
        ],
        cwd=FOOOCUS_FULL_DIR,
    )


def main():
    version = get_fooocus_version()
    print(f"Fooocus version: {version}")

    clone_fooocus_full(version)
    start_fooocus_api()
    start_fooocus_full()

    print(f"\nServers starting:")
    print(f"  Fooocus API: http://localhost:{FOOOCUS_API_PORT}")
    print(f"  Full Fooocus: http://localhost:{FOOOCUS_FULL_PORT}")


if __name__ == "__main__":
    main()
