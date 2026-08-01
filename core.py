from pathlib import Path

def fill_template(pattern: str, values: dict[str, str]) -> str:
    folder_name = pattern
    for old_token, new_token in values.items():
        folder_name = folder_name.replace(f"[{old_token}]", new_token)
    return folder_name

def fill_for_channels(pattern: str, values: dict[str, str], channels: list[str]) -> list[str]:
    folder_list = []
    for channel in channels:
        channel_values = {**values, "canaux": channel}
        folder_list.append(fill_template(pattern, channel_values))
    return folder_list

def build_all(catalog: dict[str, str], values: dict[str, str], selection: dict[str, list[str]]) -> list[str]:
    child_folder_names = []
    for delivery, channels in selection.items():
        pattern = catalog[delivery]
        child_folder_names.extend(fill_for_channels(pattern, values, channels))
    return child_folder_names

def plan_job(parent_pattern: str, catalog: dict[str, str], values: dict[str, str], selection: dict[str, list[str]]) -> dict[str, str]:
    parent_folder_name = fill_template(parent_pattern, values)
    child_folder_names = build_all(catalog, values, selection)
    return {"parent": parent_folder_name, "children": child_folder_names}

def create_folders(job: dict, destination: Path) -> None:
    parent_path = destination / job["parent"]
    parent_path.mkdir(parents=True, exist_ok=True)
    for child in job["children"]:
        (parent_path / child).mkdir(parents=True, exist_ok=True)