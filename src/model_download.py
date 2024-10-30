import requests
from config import Config
from pathlib import Path

class ModelDownloader:
    def __init__(self, model_url: str):
        self.model_url = model_url
        self.filename = model_url.split("/")[-1]

    def get_download_filepath(self) -> Path:
        return Config.Storage.tmp_dir / self.filename

    def download_model(self):
        filepath = self.get_download_filepath()
        try:
            response = requests.get(self.model_url)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Failed to download model: {e}")

        with open(filepath, "wb") as f:
            f.write(response.content)
            
        print(f"Model downloaded successfully and saved as {filepath}.")


