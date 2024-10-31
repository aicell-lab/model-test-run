import subprocess
from typing import Dict
from data.model_values import ModelValues
from packing.conda_file_handler import CondaFileHandler

class CondaEnvController:
    def __init__(self, model_yaml: Dict):
        self.values = ModelValues.from_dict(model_yaml)
        self.file_handler = CondaFileHandler(model_yaml)

    def create_conda_env(self):
        self.file_handler.dump_model_yaml()
        print(f"Creating conda environment from {self.file_handler.get_model_yaml_path()}...")
        self._run_create_env_process()

    def remove_conda_env(self):
        print(f"Removing existing conda environment '{self.values.name}' if it exists...")
        try:
            self._run_remove_env_process()
            print(f"Removed existing conda environment '{self.values.name}'.")
        except subprocess.CalledProcessError:
            print(f"No existing environment '{self.values.name}' found.")

    def install_dependencies(self):
        self.file_handler.dump_dependencies_yaml()
        print(f"Installing dependencies for conda environment '{self.values.name}'...")
        try:
            self._run_update_env_process()
            print(f"Dependencies installed successfully in '{self.values.name}'.")
        except subprocess.CalledProcessError as e:
            print(f"Error occurred while installing dependencies: {e}")
            raise
    
    def _run_create_env_process(self):
        subprocess.run(
            ["conda", "env", "create", "-f", str(self.file_handler.get_model_yaml_path()), "-n", self.values.name],
            check=True
        )
    
    def _run_remove_env_process(self):
        subprocess.run(
                ["conda", "env", "remove", "--name", self.values.name, "--yes"],
                check=True
            )
    
    def _run_update_env_process(self):
        subprocess.run(
                ["conda", "env", "update", "--file", str(self.file_handler.get_dependencies_path()), "--name", self.values.name],
                check=True
            )

