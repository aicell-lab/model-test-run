
from data.model_values import ModelValues
from typing import Dict
from config import Config
from pathlib import Path

import requests
from zipfile import ZipFile
from io import BytesIO
from data.model_values import ModelValues
from typing import Dict
from config import Config


class RecordFileHandler:

    def __init__(self, model_yaml: Dict):
        self.values = ModelValues.from_dict(model_yaml)
        self._create_files_dir()

    def _get_record_files_download_link(self) -> str:
        return f"https://zenodo.org/api/records/{self.values.zenodo.revision_id}/files-archive"
    
    def _create_files_dir(self):
        self._get_files_dir().mkdir(parents=True, exist_ok=True)

    def _get_files_dir(self) -> Path:
        return Config.Storage.tmp_dir / self.values.zenodo.dataset_id
    
    def get_weights_source_path(self) -> Path:
        return self._get_files_dir() / self.values.weights[0].source
    
    def download_and_extract_files(self):
        response = requests.get(self._get_record_files_download_link(), stream=True)
        response.raise_for_status()
        with ZipFile(BytesIO(response.content)) as zip_file:
            for member in zip_file.namelist():
                target_path = self._get_files_dir() / member
                try:
                    target_path.relative_to(self._get_files_dir())
                except ValueError:
                    raise Exception(f"Unsafe file path detected: {member}")
            zip_file.extractall(self._get_files_dir())
        
