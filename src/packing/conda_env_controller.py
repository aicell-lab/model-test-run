import subprocess
from typing import Dict
from data.model_values import ModelValues
from packing.conda_file_handler import CondaFileHandler
from packing.model_project import ModelProject

class CondaEnvController:
    def __init__(self, project: ModelProject):
        self.env_name = project.get_model_values().name
        self.file_handler = CondaFileHandler(project)

    def create_conda_env(self):
        self.file_handler.dump_model_yaml()
        print(f"Creating conda environment from {self.file_handler.get_model_yaml_path()}...")
        self._run_create_env_process()

    def remove_conda_env(self):
        print(f"Removing existing conda environment '{self.env_name}' if it exists...")
        try:
            self._run_remove_env_process()
            print(f"Removed existing conda environment '{self.env_name}'.")
        except subprocess.CalledProcessError:
            print(f"No existing environment '{self.env_name}' found.")

    def install_dependencies(self):
        self.file_handler.dump_dependencies_yaml()
        print(f"Installing dependencies for conda environment '{self.env_name}'...")
        try:
            self._run_update_env_process()
            print(f"Dependencies installed successfully in '{self.env_name}'.")
        except subprocess.CalledProcessError as e:
            print(f"Error occurred while installing dependencies: {e}")
            raise
    
    def _run_create_env_process(self):
        subprocess.run(
            ["conda", "env", "create", "-f", str(self.file_handler.get_model_yaml_path()), "-n", self.env_name],
            check=True
        )
    
    def _run_remove_env_process(self):
        subprocess.run(
                ["conda", "env", "remove", "--name", self.env_name, "--yes"],
                check=True
            )
    
    def _run_update_env_process(self):
        subprocess.run(
                ["conda", "env", "update", "--file", str(self.file_handler.get_dependencies_path()), "--name", self.env_name],
                check=True
            )

