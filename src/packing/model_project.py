from pydantic import HttpUrl
import requests
from typing import Optional, Dict, Any
from pathlib import Path
from config import Config
import zipfile
import yaml
from data.model_values import ModelValues

class ModelProject:
    def __init__(self, model_url: HttpUrl):
        self.model_url = model_url
        self.download_path = self.download_model()
        self.project_path = self.unpack_zip()

    def _load_yaml(self, file_path: Path) -> Any:
        try:
            with file_path.open("r") as file:
                return yaml.safe_load(file)
        except FileNotFoundError:
            print(f"File not found: {file_path}")
        except yaml.YAMLError as e:
            print(f"Error parsing YAML file: {e}")

    def get_model_yaml(self) -> Dict:
        return self._load_yaml(self.get_rdf_yaml_path())
    
    def get_model_values(self) -> ModelValues:
        return ModelValues.from_dict(self.get_model_yaml())

    def get_project_path(self) -> Path:
        return self.project_path

    def get_rdf_yaml_path(self) -> Path:
        return self.project_path / "rdf.yaml"

    def _get_unpack_dir(self) -> Optional[Path]:
        if not self.download_path:
            print("No model file to unpack.")
            return None
        if not self.download_path.suffix == '.zip':
            print(f"The downloaded file is not a zip file: {self.download_path}")
            return None
        unpack_dir = self.download_path.parent / self.download_path.stem
        unpack_dir.mkdir(parents=True, exist_ok=True)
        return unpack_dir
    
    def _extract_zipped_files(self, unpack_dir: Path):
        with zipfile.ZipFile(self.download_path, 'r') as zip_ref:
            unpack_dir_abs = unpack_dir.resolve()
            for member in zip_ref.infolist():
                member_path = unpack_dir / member.filename
                member_path_abs = member_path.resolve()
                if not member_path_abs.is_relative_to(unpack_dir_abs):
                    print(f"Skipping extraction of {member.filename} due to path traversal risk.")
                    continue
                zip_ref.extract(member, path=unpack_dir)
            print(f"Model unpacked to {unpack_dir}")

    def unpack_zip(self) -> Optional[Path]:
        unpack_dir = self._get_unpack_dir()
        try:
            self._extract_zipped_files(unpack_dir)
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
        
