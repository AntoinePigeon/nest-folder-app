from pathlib import Path
from core import create_folders, plan_job

parent_folder_pattern = "[nomdetravail]_[episode]_[distinction]_[langue]_[ref]_livrables_audio_[cadence]_[version_ss]_[date]"

catalog = {
    "mix": "[nomdetravail]_[episode]_[distinction]_[langue]_[ref]_mix_[canaux]_[niveau]_[cadence]_[version_ss]_[date]",
    "dial": "[nomdetravail]_[episode]_[distinction]_[langue]_[ref]_stem_dial_[canaux]_[niveau]_[cadence]_[version_ss]_[date]"
}

selection = {
    "mix": ["51", "loro"],
    "dial": ["loro", "mono"]
}

values = {
    "nomdetravail": "indefendable-5",
    "episode": "120",
    "distinction": "tva",
    "langue": "fr",
    "ref": "ref01",
    "niveau": "a85",
    "cadence": "23fps",
    "version_ss": "ss01",
    "date": "20260720"
}

if __name__ == "__main__":
    create_folders(plan_job(parent_folder_pattern, catalog, values, selection), Path.home() / "Desktop" )