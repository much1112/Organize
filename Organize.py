import json
import Upload
import Rename
import Locate

json_path = r"O:\Download\Organize.json"

with open(json_path, "r") as file:
    configJson = json.load(file)

base_dir = "O:\Download"

Locate.main(base_dir, configJson)
Rename.main(base_dir, configJson)
