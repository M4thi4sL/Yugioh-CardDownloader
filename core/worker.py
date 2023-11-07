from PyQt6.QtCore import QThread, pyqtSignal
import requests
import os
from .logger import logger


class DownloadWorker(QThread):
    update_progress = pyqtSignal(int)
    download_finished = pyqtSignal(bool)

    def __init__(self, data, card_dir, force):
        super().__init__()
        self.data = data
        self.card_dir = card_dir
        self.force = force
        self.interrupted = False

    def run(self):
        for key, card in enumerate(self.data):
            if self.isInterruptionRequested():
                self.interrupted = True  # Set the interrupted flag to True
                break  # Exit the loop if the thread is interrupted

            self.download_image(card, self.card_dir, force=self.force)
            self.update_progress.emit(key + 1)  # Update progress
        self.download_finished.emit(self.interrupted)

    def download_image(self, card, output_dir, force=False):
        if "image_url" in card["card_images"][0]:
            card_id = card["id"]
            url = card["card_images"][0]["image_url"]
            extension = url.split(".")[-1]

            image_path = os.path.join(output_dir, f"{card_id}.{extension}")

            if not force:
                # Check if the file already exists and skip if it does
                if os.path.exists(image_path):
                    logger.info(
                        f"Image for {card['name']} already exists, skipping download."
                    )
                    return
            try:
                response = requests.get(url, headers={"User-Agent": "Your User Agent"})
                response.raise_for_status()  # Check for HTTP status code errors

                if response.status_code == 200:
                    with open(image_path, "wb") as img_file:
                        img_file.write(response.content)
                    logger.info(f"Downloaded image {card['id']} ({card['name']})")
                else:
                    logger.warning(
                        f"Failed to download image for {card['name']} (HTTP status code: {response.status_code})"
                    )
            except Exception as e:
                logger.error(f"Error downloading image for {card['name']}: {str(e)}")
