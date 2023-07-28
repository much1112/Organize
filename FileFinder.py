import os


find = ".jpg"


def process_file(file_path):
    # Replace this function with the actual logic to process each file
    if find in file_path:
        print("Processing file:", file_path)


def process_folder(folder_path):
    for entry in os.scandir(folder_path):
        if entry.is_file():
            process_file(entry.path)
        elif entry.is_dir():
            process_folder(entry.path)


def main():
    root_folder = "O:/Download"
    process_folder(root_folder)


if __name__ == "__main__":
    main()
