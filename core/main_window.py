import os
import json

from PyQt6.QtWidgets import (
    QMainWindow,
    QProgressBar,
    QVBoxLayout,
    QPushButton,
    QWidget,
    QHBoxLayout,
    QMessageBox,
    QDialog,
)
from PyQt6.QtGui import QIcon, QColor, QPalette
from PyQt6.QtCore import QThread, Qt, pyqtSignal, QSize

from .settings import SettingsDialog
from .worker import DownloadWorker


class CardImageDownloaderApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.worker = None
        self._force_download = False

    def init_ui(self):
        self.setWindowTitle("YGO Image Downloader")
        self.setFixedSize(400, 100)  # Set a fixed size
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        icon = QIcon(
            "resources\\icons\\icon.png"
        )  # Replace with the actual path to your icon image
        self.setWindowIcon(icon)

        self.layout = QVBoxLayout()

        # Create a progress bar
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setValue(0)  # Initialize the progress bar
        self.layout.addWidget(self.progress_bar)

        # Create a horizontal layout for the bottom part
        bottom_layout = QHBoxLayout()

        # start download button
        self.start_button = QPushButton("Download", self)
        self.start_button.setIcon(
            QIcon("resources\\icons\\downloads.png")
        )  # Replace with the path to your icon
        self.start_button.setToolTip("Click to start downloading card images")
        self.start_button.clicked.connect(self.start_download)
        bottom_layout.addWidget(self.start_button)

        # settings button
        self.settings_button = QPushButton(self)
        settings_icon = QIcon(
            "resources\\icons\\settings.png"
        )  # Replace with the path to your settings icon

        self.settings_button.setIcon(
            QIcon(settings_icon)
        )  # Replace with the path to your settings icon
        self.settings_button.setToolTip("Click to open the settings window")
        self.settings_button.setIconSize(
            QSize(settings_icon.actualSize(QSize(20, 20)))
        )  # Set the size based on the icon
        self.settings_button.setFixedSize(
            self.settings_button.iconSize()
        )  # Set the button size to match the icon
        self.settings_button.setStyleSheet("border: none; outline: none;")
        self.settings_button.clicked.connect(self.open_settings)
        bottom_layout.addWidget(self.settings_button)

        # Add the horizontal layout for the bottom part to the main vertical layout
        self.layout.addLayout(bottom_layout)

        self.central_widget.setLayout(self.layout)

    def start_download(self):
        if self.worker is None or not self.worker.isRunning():
            force = SettingsDialog(self).get_force_download()
            json_file = "resources\\php\\cardinfo.php"
            if not os.path.exists(json_file):
                QMessageBox.critical(
                    None,
                    "Error",
                    f"File '{json_file}' not found in the current directory.",
                )
                return

            with open(json_file, "r") as file:
                data = json.load(file)["data"]

            num_entries = len(data)  # Calculate the number of entries

            self.progress_bar.setValue(0)  # Reset the progress bar to the initial value
            self.progress_bar.setMaximum(
                num_entries
            )  # Set the maximum value to the number of entries

            card_dir = ".\\cards"
            os.makedirs(card_dir, exist_ok=True)

            self.worker = DownloadWorker(data, card_dir, force)
            self.worker.update_progress.connect(self.update_progress)
            self.worker.download_finished.connect(self.download_finished)
            self.worker.start()

    def update_progress(self, value):
        self.progress_bar.setValue(value)
        self.update_title(
            value, self.progress_bar.maximum()
        )  # Update the title based on the progress

    def update_title(self, current, total):
        new_title = f"YGO Image Downloader ({current} / {total})"
        self.setWindowTitle(new_title)  # Set the window title directly

    def open_settings(self):
        settings_dialog = SettingsDialog(self).exec()

    def download_finished(self):
        self.worker = None
        QMessageBox.information(None, "Download Complete", "Download finished.")
