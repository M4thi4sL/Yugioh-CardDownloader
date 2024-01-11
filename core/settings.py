from PySide6.QtWidgets import (
    QDialog,
    QPushButton,
    QCheckBox,
    QVBoxLayout,
    QHBoxLayout,
    QFormLayout,
    QFileDialog,
)
import configparser


class SettingsManager:
    def __init__(self):
        self.config = configparser.ConfigParser()

    def save_settings(self, force_download, card_dir):
        # Set the values in the config parser
        self.config["Settings"] = {
            "force_download": str(force_download),
            "card_dir": card_dir,
        }

        # Specify the path to your .ini file
        ini_file_path = ".\\config.ini"

        # Write the configuration to the .ini file
        with open(ini_file_path, "w") as configfile:
            self.config.write(configfile)

    def load_settings(self):
        # Specify the path to your .ini file
        ini_file_path = ".\\config.ini"

        # Read the configuration from the .ini file
        self.config.read(ini_file_path)

        if "Settings" in self.config:
            settings = self.config["Settings"]
            force_download = settings.getboolean("force_download", False)
            card_dir = settings.get("card_dir", "")
            return force_download, card_dir
        else:
            return False, ""


class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Settings")

        layout = QVBoxLayout()
        settings_layout = QFormLayout()

        # declare settings
        self.force_checkbox = QCheckBox("Force Download", self)
        settings_layout.addRow(self.force_checkbox)

        # Replace the QLineEdit with a QPushButton for selecting the directory
        self.card_dir_button = QPushButton("Select Directory", self)
        self.card_dir_button.clicked.connect(self.select_card_directory)
        settings_layout.addRow("Card Directory", self.card_dir_button)

        # Load the settings when the Settings window is opened
        self.load_settings()

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
        apply_button.clicked.connect(self.save_settings)
        bottom_layout.addWidget(apply_button)

        # Add a "Revert" button
        revert_button = QPushButton("Revert", self)
        revert_button.clicked.connect(self.revert_settings)
        bottom_layout.addWidget(revert_button)

        default_button = QPushButton("Defaults", self)
        default_button.clicked.connect(self.load_default_settings)
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
        return self.card_dir_button.text()

    def set_card_dir(self, card_dir):
        # Set the value of the card directory setting
        self.card_dir_button.setText(card_dir)

    def save_settings(self):
        settings_manager = SettingsManager()
        force_download = self.get_force_download()
        card_dir = self.get_card_dir()
        settings_manager.save_settings(force_download, card_dir)

    def load_settings(self):
        settings_manager = SettingsManager()
        force_download, card_dir = settings_manager.load_settings()

        self.set_force_download(force_download)
        self.set_card_dir(card_dir)
        return force_download, card_dir

    def load_default_settings(self):
        settings_manager = SettingsManager()
        self.set_force_download(False)
        self.set_card_dir(".\\cards")
        self.save_settings()

    def revert_settings(self):
        # Load and revert to the previously saved settings
        force_download, card_dir = self.load_settings()
        self.set_force_download(force_download)
        self.set_card_dir(card_dir)

    def select_card_directory(self):
        options = QFileDialog.Option.ShowDirsOnly

        selected_directory = QFileDialog.getExistingDirectory(
            self, "Select Card Directory", self.card_dir_button.text(), options=options
        )

        if selected_directory:
            # Update the button text with the selected directory
            self.card_dir_button.setText(selected_directory)
