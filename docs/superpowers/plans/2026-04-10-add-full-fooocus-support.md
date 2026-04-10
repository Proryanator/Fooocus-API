# Add Full Fooocus Support Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a `-f` flag to `run.sh` that clones the official Fooocus repo (matching version from `fooocus_version.py`) to `repositories/fooocus-full` and runs both the full Fooocus UI and Fooocus API servers.

**Architecture:** A Python script handles version reading, cloning (if needed), and starting both servers. The shell script parses the `-f` flag and delegates to Python.

**Tech Stack:** Python (cross-platform), Shell (bash)

---

### Task 1: Create the Python helper script

**Files:**
- Create: `scripts/clone_and_run_full_fooocus.py`

- [ ] **Step 1: Create the Python script**

```python
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

REPOS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "repositories")
FOOOCUS_API_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FOOOCUS_VERSION_FILE = os.path.join(REPOS_DIR, "Fooocus", "fooocus_version.py")
FOOOCUS_FULL_DIR = os.path.join(REPOS_DIR, "fooocus-full")
FOOOCUS_REPO_URL = "https://github.com/lllyasviel/Fooocus.git"
FOOOCUS_API_PORT = "8888"
FOOOCUS_FULL_PORT = "7865"


def get_fooocus_version():
    """Read version from fooocus_version.py"""
    with open(FOOOCUS_VERSION_FILE, 'r') as f:
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
        ["git", "clone", "--depth", "1", "--branch", f"v{version}", FOOOCUS_REPO_URL, FOOOCUS_FULL_DIR],
        check=True
    )
    print(f"Cloned Fooocus v{version} to {FOOOCUS_FULL_DIR}")


def start_fooocus_api():
    """Start Fooocus API server."""
    print("Starting Fooocus API on port 8888...")
    conda_env = os.environ.get("CONDA_DEFAULT_ENV", "fooocus-api")
    subprocess.Popen(
        ["conda", "run", "-n", conda_env, "--live-stream", "python", "main.py", "--host", "0.0.0.0"],
        cwd=FOOOCUS_API_DIR
    )


def start_fooocus_full():
    """Start full Fooocus web UI server."""
    print("Starting Full Fooocus on port 7865...")
    conda_env = os.environ.get("CONDA_DEFAULT_ENV", "fooocus-api")
    # Full Fooocus uses python entrypoint.py with port flag
    subprocess.Popen(
        ["conda", "run", "-n", conda_env, "--live-stream", "python", "entrypoint.py", "--port", FOOOCUS_FULL_PORT, "--host", "0.0.0.0"],
        cwd=FOOOCUS_FULL_DIR
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
```

- [ ] **Step 2: Make the script executable**

Run: `chmod +x scripts/clone_and_run_full_fooocus.py`

---

### Task 2: Modify run.sh to support `-f` flag

**Files:**
- Modify: `run.sh`

- [ ] **Step 1: Update run.sh**

```bash
#!/bin/bash

# Get local IP
LOCAL_IP=$(ipconfig getifaddr en0 || ipconfig getifaddr en1)

# Parse flags
RUN_FULL=0
while getopts "f" opt; do
  case $opt in
    f)
      RUN_FULL=1
      ;;
    \?)
      echo "Invalid option: -$OPTARG" >&2
      exit 1
      ;;
  esac
done

echo "======================================"
if [ "$RUN_FULL" -eq 1 ]; then
    echo "Starting Fooocus API with Full Fooocus..."
    echo "Fooocus API will be accessible at: http://$LOCAL_IP:8888"
    echo "Full Fooocus will be accessible at: http://$LOCAL_IP:7865"
else
    echo "Starting Fooocus API..."
    echo "It will be accessible on your network at:"
    echo "http://$LOCAL_IP:8888"
fi
echo "======================================"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if [ "$RUN_FULL" -eq 1 ]; then
    # Run both servers via Python script
    python "$SCRIPT_DIR/scripts/clone_and_run_full_fooocus.py"
else
    # just starts the server for you; run setup.sh if you have not done so already
    conda run -n fooocus-api --live-stream python main.py --host 0.0.0.0
fi
```

- [ ] **Step 2: Test the script**

Run: `./run.sh -f`
Expected: Clone (if needed) and start both servers

---

### Task 3: Verify both servers work

- [ ] **Step 1: Run the modified run.sh with -f flag**

Run: `./run.sh -f`

- [ ] **Step 2: Check both servers are accessible**

- API: http://localhost:8888
- Full Fooocus: http://localhost:7865