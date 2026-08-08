from pathlib import Path


def analyze_storage(folder_path):
    folder = Path(folder_path)

    categories = {
        "Documents": 0,
        "Images": 0,
        "Videos": 0,
        "Others": 0
    }

    for file in folder.rglob("*"):

        if not file.is_file():
            continue

        extension = file.suffix.lower()
        size = file.stat().st_size

        if extension in [".txt", ".pdf", ".doc", ".docx"]:
            categories["Documents"] += size

        elif extension in [".jpg", ".jpeg", ".png", ".gif"]:
            categories["Images"] += size

        elif extension in [".mp4", ".mkv", ".avi"]:
            categories["Videos"] += size

        else:
            categories["Others"] += size

    return categories