import sys
from datetime import date
from PySide6.QtWidgets import QApplication, QWidget, QLineEdit, QFormLayout, QPushButton, QMessageBox, QGroupBox, QHBoxLayout, QVBoxLayout, QCheckBox
from pathlib import Path
from core import plan_job, create_folders

today = date.today()
today_string = today.strftime("%Y%m%d")

TOKENS = ["nomdetravail", "episode", "distinction", "langue", "ref", "niveau", "cadence", "version_ss", "date"]

DEFAULTS = {
    "date": today_string,
}

CHANNELS = ["51", "loro", "mono"]

parent_pattern = "[nomdetravail]_[episode]_[distinction]_[langue]_ref[ref]_livrables_audio_[cadence]_ss[version_ss]_[date]"

catalog = {
    "mix": "[nomdetravail]_[episode]_[distinction]_[langue]_ref[ref]_mix_[canaux]_[niveau]_[cadence]_ss[version_ss]_[date]",
    "dial": "[nomdetravail]_[episode]_[distinction]_[langue]_ref[ref]_stem_dial_[canaux]_[cadence]_ss[version_ss]_[date]",
    "fx": "[nomdetravail]_[episode]_[distinction]_[langue]_ref[ref]_stem_fx_[canaux]_[cadence]_ss[version_ss]_[date]",
    "mus": "[nomdetravail]_[episode]_[distinction]_[langue]_ref[ref]_stem_mus_[canaux]_[cadence]_ss[version_ss]_[date]",
    "mix_no_dial": "[nomdetravail]_[episode]_[distinction]_[langue]_ref[ref]_mix_no_dial_[canaux]_[cadence]_ss[version_ss]_[date]",
    "mix_no_mus": "[nomdetravail]_[episode]_[distinction]_[langue]_ref[ref]_mix_no_mus_[canaux]_[cadence]_ss[version_ss]_[date]",
    "mix_no_vo": "[nomdetravail]_[episode]_[distinction]_[langue]_ref[ref]_mix_no_vo_[canaux]_[cadence]_ss[version_ss]_[date]",
    "mix_undipped": "[nomdetravail]_[episode]_[distinction]_[langue]_ref[ref]_mix_undipped_[canaux]_[cadence]_ss[version_ss]_[date]",
    "mix_vd": "[nomdetravail]_[episode]_[distinction]_[langue]_ref[ref]_mix_vd_[canaux]_[niveau]_[cadence]_ss[version_ss]_[date]",
    "mne": "[nomdetravail]_[episode]_[distinction]_[langue]_ref[ref]_mne_[canaux]_[cadence]_ss[version_ss]_[date]",
    "mne_opt_dial": "[nomdetravail]_[episode]_[distinction]_[langue]_ref[ref]_mne_opt_dial_[canaux]_[cadence]_ss[version_ss]_[date]",
    "mne_opt_walla": "[nomdetravail]_[episode]_[distinction]_[langue]_ref[ref]_mne_opt_walla_[canaux]_[cadence]_ss[version_ss]_[date]",
    "mne_opt_fffx": "[nomdetravail]_[episode]_[distinction]_[langue]_ref[ref]_mne_opt_fffx_[canaux]_[cadence]_ss[version_ss]_[date]",
    "dial_no_vo": "[nomdetravail]_[episode]_[distinction]_[langue]_ref[ref]_stem_dial_no_vo_[canaux]_[cadence]_ss[version_ss]_[date]",
    "vo": "[nomdetravail]_[episode]_[distinction]_[langue]_ref[ref]_stem_vo_[canaux]_[cadence]_ss[version_ss]_[date]",
    "mus_score": "[nomdetravail]_[episode]_[distinction]_[langue]_ref[ref]_stem_mus_score_[canaux]_[cadence]_ss[version_ss]_[date]",
    "mus_stock": "[nomdetravail]_[episode]_[distinction]_[langue]_ref[ref]_stem_mus_stock_[canaux]_[cadence]_ss[version_ss]_[date]",
    "mus_undipped": "[nomdetravail]_[episode]_[distinction]_[langue]_ref[ref]_stem_mus_undipped_[canaux]_[cadence]_ss[version_ss]_[date]",
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
        if default is not None:
            field.setText(default)
        layout.addRow(token, field)
        fields[token] = field

    registry = {}
    for delivery_item in catalog:
        group = QGroupBox(delivery_item)
        group.setCheckable(True)
        group.setChecked(False)
        inner = QHBoxLayout(group) # Use QVBoxLayout for vertical layout
        channel_boxes = {}
        for channel in CHANNELS:
            checkbox = QCheckBox(channel)
            inner.addWidget(checkbox)
            channel_boxes[channel] = checkbox
        layout.addRow(group)
        registry[delivery_item] = {"box": group, "channels": channel_boxes}

    submit_btn = QPushButton("Generate")
    layout.addRow(submit_btn)

    def warn(message, title="Warning!"):
        QMessageBox.warning(window, title, message)

    def on_generate():
        values = {token: field.text().strip() for token, field in fields.items()}
        empty_tokens = [token for token, value in values.items() if not value]
        selection = {}
        for item, parts in registry.items():
            if not parts["box"].isChecked():
                continue
            checked_channels = [ch for ch, cb in parts["channels"].items() if cb.isChecked()]
            selection[item] = checked_channels
        empty_channels = [item for item, chans in selection.items() if not chans]
        if empty_tokens:
            message = "\n".join(empty_tokens)
            warn(f"Missing info in:\n\n{message}")
            return
        if not selection:
            warn("No delivery selected")
            return
        if empty_channels:
            message = "\n".join(empty_channels)
            warn(f"Missing channel in:\n\n{message}")
            return
        job = plan_job(parent_pattern, catalog, values, selection)
        create_folders(job, Path.home() / "Desktop")

    submit_btn.clicked.connect(on_generate)

    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()