import os
import shutil
import json
import datetime
import Upload

json_path = r"O:\Download\Organize.json"

with open(json_path, "r") as file:
    file_to_folder = json.load(file)

base_dir = "O:\Download"

for folder, config in file_to_folder.items():
    os.makedirs(os.path.join(base_dir, folder), exist_ok=True)
    for file in os.listdir(base_dir):
        is_not_correct_type = not any(file.endswith(ext) for ext in config["Types"])
        if is_not_correct_type:
            continue
        shutil.move(os.path.join(base_dir, file), os.path.join(base_dir, folder, file))


def Rename_date(category, types):
    category_path = os.path.join(base_dir, category)
    os.chdir(category_path)
    for file in os.listdir():
        is_not_correct_type = not any(file.endswith(ext) for ext in types)

        if is_not_correct_type:
            continue

        creation_date = datetime.datetime.fromtimestamp(os.path.getctime(file))
        unique_id = creation_date.strftime("%y%m%d-%H%M")
        new_path = f"{unique_id}{os.path.splitext(file)[1]}"
        os.rename(file, new_path)


for folder, config in file_to_folder.items():
    if config.get("Rename_date"):
        Rename_date(folder, config["Types"])

Upload.main()
