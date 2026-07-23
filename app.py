import sys
from datetime import date
from PySide6.QtWidgets import QApplication, QWidget, QLineEdit, QFormLayout, QPushButton
from pathlib import Path
from core import plan_job, create_folders

today = date.today()
today_string = today.strftime("%Y%m%d")

TOKENS = ["nomdetravail", "episode", "distinction", "langue", "ref", "niveau", "cadence", "version_ss", "date"]

DEFAULTS = {
    "date": today_string,
}

parent_pattern = "[nomdetravail]_[episode]_[distinction]_[langue]_ref[ref]_livrables_audio_[cadence]_ss[version_ss]_[date]"

catalog = {
    "mix": "[nomdetravail]_[episode]_[distinction]_[langue]_ref[ref]_mix_[canaux]_[niveau]_[cadence]_ss[version_ss]_[date]",
    "dial": "[nomdetravail]_[episode]_[distinction]_[langue]_ref[ref]_stem_dial_[canaux]_[cadence]_ss[version_ss]_[date]"
}

selection = {
    "mix": ["51", "loro"],
    "dial": ["loro", "mono"]
}

def main():
    app = QApplication(sys.argv)

    window = QWidget()
    window.setWindowTitle("Nest")
    window.resize(400, 400)

    layout = QFormLayout(window)

    fields = {}
    for token in TOKENS:
        field = QLineEdit()
        default = DEFAULTS.get(token)
        if default:
            field.setText(default)
        layout.addRow(token, field)
        fields[token] = field


    submit_btn = QPushButton("Generate")
    layout.addRow(submit_btn)

    def on_generate():
        values = {token: field.text() for token, field in fields.items()}
        job = plan_job(parent_pattern, catalog, values, selection)
        print(job)
        create_folders(job, Path.home() / "Desktop")

    submit_btn.clicked.connect(on_generate)

    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()