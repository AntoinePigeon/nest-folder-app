import sys
from datetime import date
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QWidget, QLineEdit, QFormLayout, QPushButton, QGroupBox, QHBoxLayout, QVBoxLayout, QCheckBox, QFileDialog, QTabWidget, QDialog, QDialogButtonBox, QStyle, QLabel
from pathlib import Path
from core import plan_job, create_folders

today = date.today()
today_string = today.strftime("%Y%m%d")

TOKENS = ["nomdetravail", "episode", "distinction", "langue", "ref", "niveau", "cadence", "version_ss", "date"]

DEFAULTS = {
    "date": today_string,
}

CHANNELS = ["51", "loro", "mono"]

PARENT_PATTERN = "[nomdetravail]_[episode]_[distinction]_[langue]_ref[ref]_livrables_audio_[cadence]_ss[version_ss]_[date]"

CATALOG = {
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

CATEGORIES = {
    "MDME": ["mix", "mix_vd", "dial", "fx", "mus"],
    "MNE": ["mne", "mne_opt_dial", "mne_opt_walla", "mne_opt_fffx"],
    "Mix Minus": ["mix_no_dial", "mix_no_mus", "mix_no_vo", "mix_undipped"],
    "Stems": ["dial_no_vo", "vo", "mus_score", "mus_stock", "mus_undipped"]
}

class NestDialog(QDialog):
    def __init__(self, message, title="Missing info", parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.resize(300, 150)

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.icon_label = QLabel()
        standard_icon = self.style().standardIcon(QStyle.StandardPixmap.SP_MessageBoxWarning)
        pixmap = standard_icon.pixmap(70, 70)
        self.icon_label.setPixmap(pixmap)
        self.icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.message_label = QLabel(message)
        self.message_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok)
        self.button_box.accepted.connect(self.accept)
        self.button_box.centerButtons() 

        layout.addWidget(self.icon_label)
        layout.addWidget(self.message_label)
        layout.addWidget(self.button_box)

class NestWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Nest")
        self.resize(750, 300)
        self.load_stylesheet()
        self.catalog = CATALOG
        self.build_ui()

    def load_stylesheet(self):
        try:
            style_path = Path(__file__).parent / "style.qss"
            text = style_path.read_text()
            self.setStyleSheet(text)
        except FileNotFoundError:
            print(f"Stylesheet not found at {style_path}")

    def build_ui(self):

        self.fields = {}
        self.registry = {}
        self.tabs = QTabWidget()
        self.build_tabs()

        form_container = QWidget()
        layout = QFormLayout(form_container)
        self.build_form(layout)
        outer_layout = QVBoxLayout(self)

        columns_layout = QHBoxLayout()
        columns_layout.addWidget(form_container)
        columns_layout.addWidget(self.tabs)
        outer_layout.addLayout(columns_layout)

        submit_btn = QPushButton("Generate")
        outer_layout.addWidget(submit_btn)
        submit_btn.clicked.connect(self.on_generate)

    def build_form(self, layout):
        for token in TOKENS:
            field = QLineEdit()
            default = DEFAULTS.get(token)
            if default is not None:
                field.setText(default)
            layout.addRow(token, field)
            self.fields[token] = field

    def build_tabs(self):
        for category, items in CATEGORIES.items():
            page = QWidget()
            page_layout = QVBoxLayout(page)

            for delivery_item in items:
                group = QGroupBox(delivery_item)
                group.setCheckable(True)
                group.setChecked(False)
                inner = QHBoxLayout(group) # Use QVBoxLayout for vertical layout
                inner.setContentsMargins(8, 10, 8, 10)
                inner.setSpacing(20)

                channel_boxes = {}
                for channel in CHANNELS:
                    checkbox = QCheckBox(channel)
                    inner.addWidget(checkbox)
                    channel_boxes[channel] = checkbox

                page_layout.addWidget(group)
                self.registry[delivery_item] = {"box": group, "channels": channel_boxes}

            page_layout.addStretch()
            self.tabs.addTab(page, category)

    def warn(self, message, title="Missing info"):
        dialog = NestDialog(message, title, parent=self)
        dialog.exec()

    def on_generate(self):
        values = {token: field.text().strip() for token, field in self.fields.items()}
        empty_tokens = [token for token, value in values.items() if not value]
        selection = {}
        for item, parts in self.registry.items():
            if not parts["box"].isChecked():
                continue
            checked_channels = [ch for ch, cb in parts["channels"].items() if cb.isChecked()]
            selection[item] = checked_channels
        empty_channels = [item for item, chans in selection.items() if not chans]
        if empty_tokens:
            missing_token = "\n".join(empty_tokens)
            self.warn(f"Missing info in:\n\n{missing_token}")
            return
        if not selection:
            self.warn("No delivery selected")
            return
        if empty_channels:
            missing_delivery = "\n".join(empty_channels)
            self.warn(f"Missing channel in:\n\n{missing_delivery}")
            return
        job = plan_job(PARENT_PATTERN, self.catalog, values, selection)
        destination = QFileDialog.getExistingDirectory(self, "Destination")
        if not destination:
            return
        create_folders(job, Path(destination))

def main():
    app = QApplication(sys.argv)
    window = NestWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()