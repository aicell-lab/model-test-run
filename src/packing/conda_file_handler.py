from config import Config
import yaml
from typing import Dict
from packing.conda_env import get_conda_env, CondaEnv
from data.model_value_converter import ModelValueConverter
from data.model_values import ModelValues
from pathlib import Path
from packing.model_project import ModelProject

class CondaFileHandler:
    def __init__(self, project: ModelProject):
        self.model_yaml = project.get_model_yaml()
        self.values = ModelValues.from_dict(self.model_yaml)
        self.project = project
        self._get_files_dir().mkdir(parents=True, exist_ok=True)

    def _get_conda_env(self) -> CondaEnv:
        weights_descr = ModelValueConverter(self.model_yaml).get_weights_descr()
        return get_conda_env(env_name=self.values.name, entry=weights_descr)

    def _get_files_dir(self) -> Path:
        return self.project.get_project_path() / "conda_files"
    
    def get_dependencies_path(self) -> Path:
        return self._get_files_dir() / f"{self.values.name}_deps.yml"

    def get_model_yaml_path(self) -> Path:
        return self._get_files_dir() / f"{self.values.name}.yml"

    def get_conda_pack_path(self):
        return self._get_files_dir() / f"{self.values.name}.tar.gz"

    def dump_dependencies_yaml(self):
        env_dependencies = self._get_conda_env()
        with open(self.get_dependencies_path(), 'w') as file:
            yaml.dump(env_dependencies, file)

    def dump_model_yaml(self):
        with open(self.get_model_yaml_path(), 'w') as file:
            yaml.dump(self.model_yaml, file)