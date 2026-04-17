#!/bin/bash

set -e

echo "===== Fooocus API Setup Script ====="

# Hardcode conda path for reliability
CONDA="$HOME/miniconda/bin/conda"

# Check for conda
if [ ! -f "$CONDA" ]; then
    echo "Conda not found. Installing Miniconda..."

    ARCH=$(uname -m)
    if [[ "$ARCH" == "arm64" ]]; then
        INSTALLER="Miniconda3-latest-MacOSX-arm64.sh"
    else
        INSTALLER="Miniconda3-latest-MacOSX-x86_64.sh"
    fi

    curl -LO https://repo.anaconda.com/miniconda/$INSTALLER
    bash $INSTALLER -b -p $HOME/miniconda

    export PATH="$HOME/miniconda/bin:$PATH"

    echo "Initializing conda..."
    $CONDA init bash
    source "$HOME/miniconda/etc/profile.d/conda.sh"
else
    echo "Conda already installed."
    source "$HOME/miniconda/etc/profile.d/conda.sh"
fi

# Accept Anaconda terms of service for channels
echo "Accepting Anaconda terms of service..."
$CONDA tos accept --override-channels --channel https://repo.anaconda.com/pkgs/main || true
$CONDA tos accept --override-channels --channel https://repo.anaconda.com/pkgs/r || true

# Create environment using conda run (no activation needed)
echo "Creating conda environment..."
$CONDA create -y -n fooocus-api python=3.10

# Optional: install torch with MPS (Mac GPU acceleration)
echo "Installing PyTorch with MPS support..."
$CONDA run -n fooocus-api --live-stream pip install torch torchvision torchaudio

# Download models using model_loader
echo "Downloading models..."
$CONDA run -n fooocus-api --live-stream python -c "from fooocusapi.utils.model_loader import download_models; download_models()"

# run the run.sh shell script
echo ""
echo "NOTE: If you get a macOS firewall prompt asking about Python accepting"
echo "incoming network connections, go to System Settings > Privacy & Security"
echo "and allow Python (python3.10) for local network access."
echo ""

./run.sh