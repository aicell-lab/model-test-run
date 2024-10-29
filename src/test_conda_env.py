import inspect
import yaml
from pathlib import Path
from conda_pack import conda_pack_service


def _get_model_yaml():
    model_yaml_file_path = Path(__file__).parent / "test_model.yml"
    with model_yaml_file_path.open('r') as file:
        return yaml.safe_load(file)

"""
Given a model yaml file, resolve it to a conda file and build an environment.
"""
def test_conda_env_creation():
    print(f"Running {inspect.currentframe().f_code.co_name}")
    conda_pack_service(_get_model_yaml())
    