from PyQt6.QtWidgets import QLineEdit, QDialog, QMainWindow, QPushButton, QCheckBox, QVBoxLayout, QHBoxLayout, QWidget, QFormLayout
from PyQt6.QtGui import QIcon, QColor, QPalette
from PyQt6.QtCore import QThread, Qt, pyqtSignal, QSize


class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Settings")

        layout = QVBoxLayout()
        settings_layout = QFormLayout()

        # declare settings
        self.force_checkbox = QCheckBox("Force Download", self)
        settings_layout.addRow(self.force_checkbox)

        self.card_dir_edit = QLineEdit(self)
        self.card_dir_edit.setPlaceholderText("Card Directory")
        settings_layout.addRow("Card Directory", self.card_dir_edit)

        # setting defaults
        # TODO write settings to .ini file upon clicking apply.
        # TODO read settings from .ini when user clicked revert (returning to previous )

        self.original_force_download = self.force_checkbox.isChecked()
        self.original_card_dir = self.card_dir_edit.text()

        # Apply alternating background colors to form layout rows
        for i in range(settings_layout.rowCount()):
            widget = settings_layout.itemAt(i).widget()
            if i % 2 == 0:
                widget.setStyleSheet("background-color: #ededed;")
            else:
                widget.setStyleSheet("background-color: #DCDCDC;")

        # Add apply and default button
        bottom_layout = QHBoxLayout()
        apply_button = QPushButton("Apply", self)
        apply_button.clicked.connect(self.accept)
        bottom_layout.addWidget(apply_button)

        default_button = QPushButton("Defaults", self)
        default_button.clicked.connect(self.default_settings)
        bottom_layout.addWidget(default_button)

        layout.addLayout(settings_layout)
        layout.addLayout(bottom_layout)

        self.setLayout(layout)
        self.setFixedSize(400, self.calculate_height())

    def calculate_height(self):
        # Calculate the height based on the number of rows in the form layout
        settings_layout = self.layout().itemAt(0).layout()
        row_height = 25  # Height of each row
        num_rows = settings_layout.rowCount()
        extra_space = 60  # Additional space for buttons and padding
        return num_rows * row_height + extra_space

    # GET / SET --force setting
    def get_force_download(self):
        # Get the state of the "Force Download" checkbox
        return self.force_checkbox.isChecked()

    def set_force_download(self, checked):
        # Set the state of the "Force Download" checkbox
        self.force_checkbox.setChecked(checked)

    def get_card_dir(self):
        # Get the value of the card directory setting
        return self.card_dir_edit.text()

    def set_card_dir(self, card_dir):
        # Set the value of the card directory setting
        self.card_dir_edit.setText(card_dir)

    def default_settings(self):
        # default the settings to their original values
        self.set_force_download(self.original_force_download)
