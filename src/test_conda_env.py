import inspect
import yaml
from pathlib import Path
from conda_env import get_conda_env, SupportedWeightsEntry
from bioimageio.spec.model import v0_4, v0_5


def _get_model_yaml():
    model_yaml_file_path = Path(__file__).parent / "test_model.yml"
    with model_yaml_file_path.open('r') as file:
        return yaml.safe_load(file)
    
def _get_weights_entry(model_yaml: dict) -> SupportedWeightsEntry:
    if not model_yaml.get('weights'):
        raise ValueError("No weights found in the model YAML.")
    
    weight_entry = model_yaml['weights'][0]
    
    if 'source' not in weight_entry or 'opset_version' not in weight_entry:
        raise ValueError("Weight entry must contain 'source' and 'opset_version'.")
   
    entry = v0_4.OnnxWeightsDescr(
        opset_version=weight_entry.get("opset_version"),
        source=weight_entry.get("source") 
    )
    return entry

"""
Given a model yaml file, resolve it to a conda file and build an environment.
"""
def test_conda_env_creation():
    print(f"Running {inspect.currentframe().f_code.co_name}")
    model_yaml = _get_model_yaml()
    conda_env = get_conda_env(env_name="test_env", entry=_get_weights_entry(model_yaml))
    print(conda_env)
    