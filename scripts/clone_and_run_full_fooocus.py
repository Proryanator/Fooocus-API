#!/usr/bin/env python3
"""
Run full Fooocus alongside Fooocus API.
Imports logic from run_full_fooocus.py to clone (if needed) and run both servers.
"""

import os
import sys

# Add scripts directory to path to import run_full_fooocus module
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, script_dir)

from run_full_fooocus import (
    get_fooocus_version,
    ensure_fooocus_full_clone,
    start_fooocus_full,
)

FOOOCUS_API_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FOOOCUS_API_PORT = "8888"


def start_fooocus_api():
    """Start Fooocus API server."""
    print("Starting Fooocus API on port 8888...")
    conda_env = os.environ.get("CONDA_DEFAULT_ENV", "fooocus-api")
    import subprocess

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


def main():
    version = get_fooocus_version()
    print(f"Fooocus version: {version}")

    ensure_fooocus_full_clone(version)
    start_fooocus_api()
    start_fooocus_full()

    print(f"\nServers starting:")
    print(f"  Fooocus API: http://localhost:{FOOOCUS_API_PORT}")
    print(f"  Full Fooocus: http://localhost:7865")


if __name__ == "__main__":
    main()
