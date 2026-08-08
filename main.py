from file_scanner import scan_folder
from file_organizer import organize_files
from duplicate_finder import find_duplicates
from storage_analyzer import analyze_storage
from search_engine import search_files

print("========================================")
print("          AI FILE ASSISTANT")
print("========================================")

print("1. Scan Folder")
print("2. Organize Files")
print("3. Find Duplicate Files")
print("4. Find Large Files")
print("5. Search Files")
print("6. Storage Analysis")
print("7. AI Assistant")
print("8. Exit")

choice = input("Enter your choice: ")

if choice == "1":
    folder_path = input("Enter folder path: ")

    files = scan_folder(folder_path)

    print("\nFiles found:")

    for file in files:
        print("Name:", file.name)
        print("Type:", file.suffix)
        print("Size:", file.stat().st_size, "bytes")
        print()

elif choice == "2":
    folder_path = input("Enter folder path: ")

    organize_files(folder_path)

elif choice == "3":
    folder_path = input("Enter folder path: ")

    duplicates = find_duplicates(folder_path)

    if duplicates:
        print("\nDuplicate files found:")

        for original, duplicate in duplicates:
            print("Original :", original)
            print("Duplicate:", duplicate)
            print()
    else:
        print("No duplicate files found.")

elif choice == "4":
    print("Finding large files...")

elif choice == "5":
    folder_path = input("Enter folder path: ")
    search_text = input("Enter file name to search: ")

    results = search_files(folder_path, search_text)

    if results:
        print("\nFiles found:")

        for file in results:
            print(file)

    else:
        print("No matching files found.")

elif choice == "6":
    folder_path = input("Enter folder path: ")

    storage = analyze_storage(folder_path)

    print("\nStorage Analysis:")

    for category, size in storage.items():
        print(category, ":", size, "bytes")

elif choice == "7":
    print("Starting AI assistant...")

elif choice == "8":
    print("Goodbye!")

else:
    print("Invalid choice.")