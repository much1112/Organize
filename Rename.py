import os
import datetime


def name(category, types, base_dir):
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


def main(base_dir, configJson):
    for folder, config in configJson.items():
        if not config.get("Rename_date"):
            continue
        name(folder, config["Types"], base_dir)
