import os
import shutil


def main(base_dir, configJson):
    for folder, config in configJson.items():
        os.makedirs(os.path.join(base_dir, folder), exist_ok=True)
        for file in os.listdir(base_dir):
            is_not_correct_type = not any(file.endswith(ext) for ext in config["Types"])
            if is_not_correct_type:
                continue
            shutil.move(
                os.path.join(base_dir, file), os.path.join(base_dir, folder, file)
            )
