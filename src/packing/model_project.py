from pydantic import HttpUrl
import requests
from typing import Tuple, List, Optional
import yaml
from pathlib import Path
from config import Config
import zipfile

class ModelProject:
    def __init__(self, model_url: HttpUrl):
        self.model_url = model_url
        self.download_path = self.download_model()
        self.project_path = self.unpack_zip()

    def unpack_zip(self) -> Optional[Path]:
        if not self.download_path:
            print("No model file to unpack.")
            return None
        if not self.download_path.suffix == '.zip':
            print(f"The downloaded file is not a zip file: {self.download_path}")
            return None
        unpack_dir = self.download_path.parent / self.download_path.stem
        unpack_dir.mkdir(parents=True, exist_ok=True)
        try:
            with zipfile.ZipFile(self.download_path, 'r') as zip_ref:
                zip_ref.extractall(unpack_dir)
                print(f"Model unpacked to {unpack_dir}")
            return unpack_dir
        except zipfile.BadZipFile:
            print(f"Failed to unpack zip file: {self.download_path}")
            return None
        
    def download_model(self) -> Optional[Path]:
        model_dir = Config.Storage.tmp_dir / "model_projects"
        model_dir.mkdir(parents=True, exist_ok=True)
        filename = Path(self.model_url).name
        download_path = model_dir / filename
        
        try:
            response = requests.get(self.model_url, stream=True)
            response.raise_for_status()
            with open(download_path, "wb") as file:
                for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)
            print(f"Model downloaded to {download_path}")
            return download_path
        except requests.RequestException as e:
            print(f"Failed to download model: {e}")
            return None
        
