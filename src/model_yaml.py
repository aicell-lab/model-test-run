from bioimageio.spec.model import v0_4, v0_5
from conda_env import SupportedWeightsEntry
from config import Config
import subprocess
import yaml
from typing import Dict
from conda_env import get_conda_env, CondaEnv
from pathlib import Path

class ModelYaml:
    FORMAT_TO_WEIGHTS_ENTRY = {
        "onnx": v0_5.OnnxWeightsDescr,
        "pytorch_state_dict": v0_5.PytorchStateDictWeightsDescr,
        "tensorflow_saved_model_bundle": v0_5.TensorflowSavedModelBundleWeightsDescr,
        "torchscript": v0_5.TorchscriptWeightsDescr,
    }

    def __init__(self, model_yaml: Dict):
        self.model_yaml = model_yaml
        self.tmp_yaml_filepath = Config.Storage.tmp_dir / f"{self.get_name()}.yml"

    def _check_weights(self):
        if not self.model_yaml.get('weights'):
            raise ValueError("No weights found in the model YAML.")
        
        required_keys = ['source', 'opset_version', 'format']
        missing_keys = [key for key in required_keys if key not in self._get_weights_entry()]
        if missing_keys:
            raise ValueError(f"Weight entry must contain the following keys: {', '.join(missing_keys)}")

    def _check_weights_format(self):
        weight_entry = self.model_yaml['weights'][0]
        if weight_entry['format'] not in self.FORMAT_TO_WEIGHTS_ENTRY:
            raise ValueError(
                f"Unsupported format '{weight_entry['format']}' found in weight entry. "
                f"Supported formats are: {', '.join(self.FORMAT_TO_WEIGHTS_ENTRY.keys())}"
            )
        
    def _get_weights_entry(self):
        return self.model_yaml['weights'][0]
    
    def _get_weights_opset_version(self):
        return self._get_weights_entry().get("opset_version")
    
    def get_weights_source(self):
        return self._get_weights_entry().get("source")
        
    def get_weights_format(self):
        return self._get_weights_entry()['format']
        
    def get_weights_descr_class(self):
        return ModelYaml.FORMAT_TO_WEIGHTS_ENTRY.get(self.get_weights_format())
    
    def get_name(self) -> str:
        return self.model_yaml.get("name").replace(" ", "_") or Config.UNKNOWN_NAME

    def get_weights_descr(self) -> SupportedWeightsEntry:
        return self.get_weights_descr_class()(
            opset_version=self._get_weights_opset_version(),
            source=self.get_weights_source()
        )

    def validate(self):
        self._check_weights()
        self._check_weights_format()

    def _dump_model_yaml(self) -> Path:
        with open(self.tmp_yaml_filepath, 'w') as file:
            yaml.dump(self.model_yaml, file)
        return self.tmp_yaml_filepath

    def create_conda_env(self):
        model_yaml_path = self._dump_model_yaml()
        print(f"Creating conda environment from {model_yaml_path}...")
        subprocess.run(
            ["conda", "env", "create", "-f", str(model_yaml_path), "-n", self.get_name()],
            check=True
        )

    def remove_conda_env(self):
        env_name = self.get_name()
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
        return get_conda_env(env_name=self.get_name(), entry=self.get_weights_descr())  
    
    def _dump_dependencies_yaml(self) -> Path:
        env_dependencies = self._get_conda_env()
        env_name = self.get_name()
        env_deps_yaml_path = Config.Storage.tmp_dir / f"{env_name}_deps.yml"
        with open(env_deps_yaml_path, 'w') as file:
            yaml.dump(env_dependencies, file)
        return env_deps_yaml_path


    def install_dependencies(self):
        env_deps_yaml_path = self._dump_dependencies_yaml()
        print(f"Installing dependencies for conda environment '{self.get_name()}'...")
        try:
            subprocess.run(
                ["conda", "env", "update", "--file", str(env_deps_yaml_path), "--name", self.get_name()],
                check=True
            )
            print(f"Dependencies installed successfully in '{self.get_name()}'.")
        except subprocess.CalledProcessError as e:
            print(f"Error occurred while installing dependencies: {e}")
            raise