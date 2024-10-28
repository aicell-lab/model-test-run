### This script may not be needed and deleted in a future commit.

import requests
from pathlib import Path

class ModelDownloader:
    def __init__(self, model_url: str):
        self.model_url = model_url
        filename = model_url.split("/")[-1]
        self.local_model_path = Path("/data") / filename # Warning: Assumed a root directory named 'data' exists.

    def download_model(self) -> None:
        """Download the model if it doesn't already exist."""
        self._check_data_directory_exists()
        if self.local_model_path.exists():
            print(f"Model already exists at {self.local_model_path}. No download needed.")
        else:
            self._request_and_store_model()

    def _request_and_store_model(self):
        try:
            response = requests.get(self.model_url)
            response.raise_for_status()
            with open(self.local_model_path, "wb") as f:
                f.write(response.content)
            print(f"Model downloaded successfully and saved as {self.local_model_path}.")
        except requests.exceptions.RequestException as e:
            print(f"Failed to download model: {e}")

    def _check_data_directory_exists(self) -> None:
        """Create the /data directory if it does not exist."""
        data_dir = Path("/data")
        if not data_dir.exists():
            try:
                data_dir.mkdir(parents=True, exist_ok=True)
                print(f"Created directory: {data_dir}")
            except Exception as e:
                print(f"Failed to create directory {data_dir}: {e}")




