from config import Config
import yaml
from typing import Dict
from packing.conda_env import get_conda_env, CondaEnv
from data.model_value_converter import ModelValueConverter
from data.model_values import ModelValues
from pathlib import Path

class CondaFileHandler:
    def __init__(self, model_yaml: Dict):
        self.values = ModelValues.from_dict(model_yaml)
        self.model_yaml = model_yaml

    def _get_conda_env(self) -> CondaEnv:
        weights_descr = ModelValueConverter(self.model_yaml).get_weights_descr()
        return get_conda_env(env_name=self.values.name, entry=weights_descr)

    def _get_files_dir(self) -> Path:
        return Config.Storage.tmp_dir
    
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