from config import Config
import subprocess
import yaml
from typing import Dict
from packing.conda_env import get_conda_env, CondaEnv
from model_yaml import ModelYaml

class CondaEnvController:
    def __init__(self, model_yaml: Dict):
        self.model_yaml_obj = ModelYaml(model_yaml)
        self._set_paths()
    
    def _set_paths(self):
        env_name = self.model_yaml_obj.get_name()
        self.tmp_model_yaml_filepath = Config.Storage.tmp_dir / f"{env_name}.yml"
        self.tmp_env_deps_yaml_path = Config.Storage.tmp_dir / f"{env_name}_deps.yml"

    def _dump_model_yaml(self):
        with open(self.tmp_model_yaml_filepath, 'w') as file:
            yaml.dump(self.model_yaml_obj.model_yaml, file)

    def create_conda_env(self):
        self._dump_model_yaml()
        print(f"Creating conda environment from {self.tmp_model_yaml_filepath}...")
        subprocess.run(
            ["conda", "env", "create", "-f", str(self.tmp_model_yaml_filepath), "-n", self.model_yaml_obj.get_name()],
            check=True
        )

    def remove_conda_env(self):
        env_name = self.model_yaml_obj.get_name()
        print(f"Removing existing conda environment '{env_name}' if it exists...")
        try:
            subprocess.run(
                ["conda", "env", "remove", "--name", env_name, "--yes"],
                check=True
            )
            print(f"Removed existing conda environment '{env_name}'.")
        except subprocess.CalledProcessError:
            print(f"No existing environment '{env_name}' found.")

    def _get_conda_env(self) -> CondaEnv:
        return get_conda_env(env_name=self.model_yaml_obj.get_name(), entry=self.model_yaml_obj.get_weights_descr())  
    
    def _dump_dependencies_yaml(self):
        env_dependencies = self._get_conda_env()
        with open(self.tmp_env_deps_yaml_path, 'w') as file:
            yaml.dump(env_dependencies, file)

    def install_dependencies(self):
        self._dump_dependencies_yaml()
        env_name = self.model_yaml_obj.get_name()
        print(f"Installing dependencies for conda environment '{env_name}'...")
        try:
            subprocess.run(
                ["conda", "env", "update", "--file", str(self.tmp_env_deps_yaml_path), "--name", env_name],
                check=True
            )
            print(f"Dependencies installed successfully in '{env_name}'.")
        except subprocess.CalledProcessError as e:
            print(f"Error occurred while installing dependencies: {e}")
            raise
