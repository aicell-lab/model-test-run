from pydantic import HttpUrl
import requests
from typing import Tuple, List, Optional
import yaml
from pathlib import Path
from config import Config


class ModelProject:
    def __init__(self, model_url: HttpUrl):
        self.model_url = model_url
        self.download_path = self.download_model() 

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
        
