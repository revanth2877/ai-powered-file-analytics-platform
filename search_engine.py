from pathlib import Path


def search_files(folder_path, search_text):
    folder = Path(folder_path)
    results = []

    for file in folder.rglob("*"):

        if not file.is_file():
            continue

        if search_text.lower() in file.name.lower():
            results.append(file)

    return results