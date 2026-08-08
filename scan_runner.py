import os

SCAN_PATH = r'C:\Users\revan\OneDrive\Desktop\test files\Documents\Documents'

def run_scan():

    total_files = 0
    total_size = 0

    for file_name in os.listdir(SCAN_PATH):

        file_path = os.path.join(SCAN_PATH, file_name)

        if os.path.isfile(file_path):

            total_files += 1
            total_size += os.path.getsize(file_path)

    return {
        'total_files': total_files,
        'duplicates': 0,
        'storage': str(round(total_size / 1024, 2)) + ' KB'
    }