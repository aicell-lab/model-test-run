import inspect
import yaml
from pathlib import Path
from conda_env import get_conda_env
from model_yaml import ModelYaml

def _get_model_yaml():
    model_yaml_file_path = Path(__file__).parent / "test_model.yml"
    with model_yaml_file_path.open('r') as file:
        return yaml.safe_load(file)

"""
Given a model yaml file, resolve it to a conda file and build an environment.
"""
def test_conda_env_creation():
    print(f"Running {inspect.currentframe().f_code.co_name}")
    model_yaml = _get_model_yaml()
    model_yaml_obj = ModelYaml(model_yaml)
    model_yaml_obj.validate()
    conda_env = get_conda_env(env_name="test_env", entry=model_yaml_obj.get_weights_descr())
    print(conda_env)
    