# -*- coding: utf-8 -*-

"""
Download models from url

@file: model_loader.py
@author: Konie
@update: 2024-03-22
"""

import json
import os
import sys

sys.path.insert(
    0,
    os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
        "repositories",
        "Fooocus",
    ),
)

from modules.model_loader import load_file_from_url


def get_preset_downloads():
    """
    Collect all checkpoint_downloads from all preset JSON files.
    This ensures models from all presets (anime, pony, realistic, etc.) are downloaded.
    """
    preset_dir = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
        "repositories",
        "Fooocus",
        "presets",
    )

    all_checkpoints = {}
    all_loras = {}
    all_embeddings = {}

    if not os.path.isdir(preset_dir):
        return all_checkpoints, all_loras, all_embeddings

    for filename in os.listdir(preset_dir):
        if not filename.endswith(".json"):
            continue

        preset_path = os.path.join(preset_dir, filename)
        try:
            with open(preset_path, "r", encoding="utf-8") as f:
                preset_data = json.load(f)

            # Merge checkpoint_downloads
            if "checkpoint_downloads" in preset_data:
                for model_name, url in preset_data["checkpoint_downloads"].items():
                    # Skip if already exists (prioritize first found)
                    if model_name not in all_checkpoints:
                        all_checkpoints[model_name] = url

            # Merge lora_downloads
            if "lora_downloads" in preset_data:
                for model_name, url in preset_data["lora_downloads"].items():
                    if model_name not in all_loras:
                        all_loras[model_name] = url

            # Merge embeddings_downloads
            if "embeddings_downloads" in preset_data:
                for model_name, url in preset_data["embeddings_downloads"].items():
                    if model_name not in all_embeddings:
                        all_embeddings[model_name] = url

        except (json.JSONDecodeError, IOError) as e:
            print(f"[Warning] Failed to read preset {filename}: {e}")
            continue

    return all_checkpoints, all_loras, all_embeddings


def download_models():
    """
    Download models from config and all presets
    """
    vae_approx_filenames = [
        (
            "xlvaeapp.pth",
            "https://huggingface.co/lllyasviel/misc/resolve/main/xlvaeapp.pth",
        ),
        (
            "vaeapp_sd15.pth",
            "https://huggingface.co/lllyasviel/misc/resolve/main/vaeapp_sd15.pt",
        ),
        (
            "xl-to-v1_interposer-v3.1.safetensors",
            "https://huggingface.co/lllyasviel/misc/resolve/main/xl-to-v1_interposer-v3.1.safetensors",
        ),
    ]

    from modules.config import (
        paths_checkpoints as modelfile_path,
        paths_loras as lorafile_path,
        path_vae_approx as vae_approx_path,
        path_fooocus_expansion as fooocus_expansion_path,
        path_embeddings as embeddings_path,
        checkpoint_downloads,
        embeddings_downloads,
        lora_downloads,
    )

    # Get downloads from all presets
    preset_checkpoints, preset_loras, preset_embeddings = get_preset_downloads()

    # Merge: config downloads take priority, then add preset downloads for new models
    merged_checkpoints = {**preset_checkpoints, **checkpoint_downloads}
    merged_loras = {**preset_loras, **lora_downloads}
    merged_embeddings = {**preset_embeddings, **embeddings_downloads}

    print(
        f"[Model Loader] Downloading {len(merged_checkpoints)} checkpoints, "
        f"{len(merged_loras)} loras, {len(merged_embeddings)} embeddings from all presets"
    )

    for file_name, url in merged_checkpoints.items():
        load_file_from_url(url=url, model_dir=modelfile_path[0], file_name=file_name)
    for file_name, url in merged_embeddings.items():
        load_file_from_url(url=url, model_dir=embeddings_path, file_name=file_name)
    for file_name, url in merged_loras.items():
        load_file_from_url(url=url, model_dir=lorafile_path[0], file_name=file_name)
    for file_name, url in vae_approx_filenames:
        load_file_from_url(url=url, model_dir=vae_approx_path, file_name=file_name)

    load_file_from_url(
        url="https://huggingface.co/lllyasviel/misc/resolve/main/fooocus_expansion.bin",
        model_dir=fooocus_expansion_path,
        file_name="pytorch_model.bin",
    )
