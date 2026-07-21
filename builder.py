# import json
# from pathlib import Path

# project_name = "TestProject"

# with open("template.json", "r") as file:
#     folder_names = json.load(file)

# for name in folder_names:
#     path = Path.home() / "Desktop" / project_name / name
#     print(path)
#     path.mkdir(parents=True, exist_ok=True)

pattern = "[nomdetravail]_[episode]_[distinction]_[langue]_[ref]_mix_[canaux]_[niveau]_[cadence]_[version_ss]_[date]"
values = {
    "nomdetravail": "indefendable-5",
    "episode": "120",
    "distinction": "tva",
    "langue": "fr",
    "ref": "ref01",
    "canaux": "5.1",
    "niveau": "a85",
    "cadence": "23fps",
    "version_ss": "ss01",
    "date": "20260720"
}

def fill_template(pattern, values):
    folder_name = pattern
    for old, new in values.items():
        folder_name = folder_name.replace(f"[{old}]", new)
    return folder_name
    
print(fill_template(pattern, values))