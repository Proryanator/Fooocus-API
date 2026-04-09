#!/bin/bash

set -e

echo "===== Fooocus API Setup Script ====="

# Check for conda
if ! command -v conda &> /dev/null
then
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
    conda init bash
    source "$HOME/miniconda/etc/profile.d/conda.sh"
else
    echo "Conda already installed."
    source "$(conda info --base)/etc/profile.d/conda.sh"
fi

# Create environment
echo "Creating conda environment..."
conda create -y -n fooocus-api python=3.10

conda activate fooocus-api

# Optional: install torch with MPS (Mac GPU acceleration)
echo "Installing PyTorch with MPS support..."
pip install torch torchvision torchaudio

# Download models using model_loader
echo "Downloading models..."
conda run -n fooocus-api --live-stream python -c "from fooocusapi.utils.model_loader import download_models; download_models()"

# run the run.sh shell script
./run.sh