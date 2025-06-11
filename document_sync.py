import json
import os
from typing import Set, Dict, List

import config


def get_processed_files(
    processed_files_path: str = "processed_files.json",
) -> Dict[str, float]:
    if not os.path.exists(processed_files_path):
        return {}
    with open(processed_files_path, "r") as f:
        return json.load(f)


def get_directory_files(directory_path: str) -> Set[str]:
    return {
        f
        for f in os.listdir(directory_path)
        if os.path.isfile(os.path.join(directory_path, f))
    }


def get_files_needing_processing(
    directory_path: str = config.WATCH_DIRECTORY,
    processed_files_path: str = "processed_files.json",
) -> List[str]:

    # Ensure the directory exists
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)

        return None

    processed_files = get_processed_files(processed_files_path)
    current_files = get_directory_files(directory_path)

    needs_processing = []

    for filename in current_files:
        filepath = os.path.join(directory_path, filename)
        current_mtime = os.path.getmtime(filepath)

        if (
            filename not in processed_files
            or processed_files[filename] != current_mtime
        ):
            needs_processing.append(filename)

    return needs_processing


def mark_file_processed(
    filename: str,
    directory_path: str = config.WATCH_DIRECTORY,
    processed_files_path: str = "processed_files.json",
):
    processed_files = get_processed_files(processed_files_path)
    filepath = os.path.join(directory_path, filename)
    processed_files[filename] = os.path.getmtime(filepath)

    with open(processed_files_path, "w") as f:
        json.dump(processed_files, f)
