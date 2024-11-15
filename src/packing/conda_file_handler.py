import yaml
from pathlib import Path
from packing.model_project import ModelProject
from typing import Union

from bioimageio.spec import ResourceDescr, InvalidDescr, ValidationContext, load_description
from bioimageio.spec.get_conda_env import get_conda_env, BioimageioCondaEnv

class CondaFileHandler:
    def __init__(self, project: ModelProject):
        self.env_name = project.get_model_values().name
        self.project = project
        self._get_files_dir().mkdir(parents=True, exist_ok=True)

    def _get_files_dir(self) -> Path:
        return self.project.get_project_path() / "conda_files"
    
    def get_dependencies_path(self) -> Path:
        return self._get_files_dir() / f"{self.env_name}_deps.yml"

    def get_model_yaml_path(self) -> Path:
        return self._get_files_dir() / f"{self.env_name}.yml"

    def get_conda_pack_path(self):
        return self._get_files_dir() / f"{self.env_name}.tar.gz"
    
    def retrieve_resource_description(self) -> Union[ResourceDescr, InvalidDescr]:
        ctx = ValidationContext(perform_io_checks=True)
        with ctx:
            rd = load_description(self.project.download_path)
        return rd
    
    @staticmethod
    def retrieve_available_weights(rd: ResourceDescr):
        return [value for _, value in rd.weights.model_dump().items() if value is not None]
    
    def retrieve_CondaEnv(self) -> BioimageioCondaEnv:
        rd = self.retrieve_resource_description()
        rd.validation_summary.display()
        if isinstance(rd, InvalidDescr):
            raise ValueError("The retrieved resource description is invalid.")
        
        print(CondaFileHandler.retrieve_available_weights(rd))
        
        env_name = self.project.get_model_values().name
        result = get_conda_env(entry=rd.weights.pytorch_state_dict, env_name=env_name) # TODO: Adapt entry input to different architecture types.
        return result

    def dump_dependencies_yaml(self):
        env_deps = self.retrieve_CondaEnv()
        with open(self.get_dependencies_path(), 'w') as file:
            yaml.dump(env_deps, file)

    def dump_model_yaml(self):
        with open(self.get_model_yaml_path(), 'w') as file:
            yaml.dump(self.project.get_model_yaml(), file)