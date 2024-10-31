from config import Config
import subprocess
import yaml
from typing import Dict
from packing.conda_env import get_conda_env, CondaEnv
from data.model_value_converter import ModelValueConverter
from data.model_values import ModelValues

class CondaEnvController:
    def __init__(self, model_yaml: Dict):
        self.values = ModelValues.from_dict(model_yaml)
        self.model_yaml = model_yaml
        self._set_paths()
    
    def _set_paths(self):
        self.tmp_model_yaml_filepath = Config.Storage.tmp_dir / f"{self.values.name}.yml"
        self.tmp_env_deps_yaml_path = Config.Storage.tmp_dir / f"{self.values.name}_deps.yml"

    def _dump_model_yaml(self):
        with open(self.tmp_model_yaml_filepath, 'w') as file:
            yaml.dump(self.model_yaml, file)

    def create_conda_env(self):
        self._dump_model_yaml()
        print(f"Creating conda environment from {self.tmp_model_yaml_filepath}...")
        subprocess.run(
            ["conda", "env", "create", "-f", str(self.tmp_model_yaml_filepath), "-n", self.values.name],
            check=True
        )

    def remove_conda_env(self):
        print(f"Removing existing conda environment '{self.values.name}' if it exists...")
        try:
            subprocess.run(
                ["conda", "env", "remove", "--name", self.values.name, "--yes"],
                check=True
            )
            print(f"Removed existing conda environment '{self.values.name}'.")
        except subprocess.CalledProcessError:
            print(f"No existing environment '{self.values.name}' found.")

    def _get_conda_env(self) -> CondaEnv:
        weights_descr = ModelValueConverter(self.model_yaml).get_weights_descr()
        return get_conda_env(env_name=self.values.name, entry=weights_descr)  
    
    def _dump_dependencies_yaml(self):
        env_dependencies = self._get_conda_env()
        with open(self.tmp_env_deps_yaml_path, 'w') as file:
            yaml.dump(env_dependencies, file)

    def install_dependencies(self):
        self._dump_dependencies_yaml()
        print(f"Installing dependencies for conda environment '{self.values.name}'...")
        try:
            subprocess.run(
                ["conda", "env", "update", "--file", str(self.tmp_env_deps_yaml_path), "--name", self.values.name],
                check=True
            )
            print(f"Dependencies installed successfully in '{self.values.name}'.")
        except subprocess.CalledProcessError as e:
            print(f"Error occurred while installing dependencies: {e}")
            raise
