from config import Config
import subprocess
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
    
    def get_dependencies_path(self) -> Path:
        return Config.Storage.tmp_dir / f"{self.values.name}_deps.yml"

    def get_model_yaml_path(self) -> Path:
        return Config.Storage.tmp_dir / f"{self.values.name}.yml"

    def dump_dependencies_yaml(self):
        env_dependencies = self._get_conda_env()
        with open(self.get_dependencies_path(), 'w') as file:
            yaml.dump(env_dependencies, file)

    def dump_model_yaml(self):
        with open(self.get_model_yaml_path(), 'w') as file:
            yaml.dump(self.model_yaml, file)

class CondaEnvController:
    def __init__(self, model_yaml: Dict):
        self.values = ModelValues.from_dict(model_yaml)
        self.file_handler = CondaFileHandler(model_yaml)
    
    def run_create_env_process(self):
        subprocess.run(
            ["conda", "env", "create", "-f", str(self.file_handler.get_model_yaml_path()), "-n", self.values.name],
            check=True
        )
    
    def run_remove_env_process(self):
        subprocess.run(
                ["conda", "env", "remove", "--name", self.values.name, "--yes"],
                check=True
            )
    
    def run_update_env_process(self):
        subprocess.run(
                ["conda", "env", "update", "--file", str(self.file_handler.get_dependencies_path()), "--name", self.values.name],
                check=True
            )

    def create_conda_env(self):
        self.file_handler.dump_model_yaml()
        print(f"Creating conda environment from {self.file_handler.get_model_yaml_path()}...")
        self.run_create_env_process()

    def remove_conda_env(self):
        print(f"Removing existing conda environment '{self.values.name}' if it exists...")
        try:
            self.run_remove_env_process()
            print(f"Removed existing conda environment '{self.values.name}'.")
        except subprocess.CalledProcessError:
            print(f"No existing environment '{self.values.name}' found.")

    def install_dependencies(self):
        self.file_handler.dump_dependencies_yaml()
        print(f"Installing dependencies for conda environment '{self.values.name}'...")
        try:
            self.run_update_env_process()
            print(f"Dependencies installed successfully in '{self.values.name}'.")
        except subprocess.CalledProcessError as e:
            print(f"Error occurred while installing dependencies: {e}")
            raise
