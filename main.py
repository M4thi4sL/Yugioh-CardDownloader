import sys
import argparse
from PySide6.QtWidgets import QApplication

from core.main_window import CardImageDownloaderApp

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--force", action="store_true", help="Skip the check for existing files"
    )
    args = parser.parse_args()
    app = QApplication(sys.argv)
    downloader_app = CardImageDownloaderApp()
    downloader_app.show()
    sys.exit(app.exec())
