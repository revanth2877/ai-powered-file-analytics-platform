from pathlib import Path
import shutil


def organize_files(folder_path):
    folder = Path(folder_path)

    for file in folder.iterdir():

        if not file.is_file():
            continue

        extension = file.suffix.lower()

        if extension in [".txt", ".pdf", ".doc", ".docx"]:
            category = "Documents"

        elif extension in [".jpg", ".jpeg", ".png", ".gif"]:
            category = "Images"

        elif extension in [".mp4", ".mkv", ".avi"]:
            category = "Videos"

        else:
            category = "Others"

        destination = folder / category

        destination.mkdir(exist_ok=True)

        shutil.move(str(file), str(destination / file.name))

        print(file.name, "→", category)

    print("Files organized successfully!")