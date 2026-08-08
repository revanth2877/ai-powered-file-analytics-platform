from pathlib import Path
import hashlib


def get_file_hash(file_path):
    hash_object = hashlib.sha256()

    with open(file_path, "rb") as file:
        while True:
            data = file.read(4096)

            if not data:
                break

            hash_object.update(data)

    return hash_object.hexdigest()


def find_duplicates(folder_path):
    folder = Path(folder_path)

    hashes = {}
    duplicates = []

    for file in folder.rglob("*"):

        if not file.is_file():
            continue

        file_hash = get_file_hash(file)

        if file_hash in hashes:
            duplicates.append((hashes[file_hash], file))
        else:
            hashes[file_hash] = file

    return duplicates