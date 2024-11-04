import inspect
import yaml
from pathlib import Path
from model_test import run_model_tests
from data.model_yaml_validation import ModelYamlValidation
from packing.conda_packer import CondaPacker

def _get_model_yaml_path():
    return Path(__file__).parent / "test_model.yml"

def _get_model_yaml():
    with _get_model_yaml_path().open('r') as file:
        return yaml.safe_load(file)

def test_services_locally():
    print(f"Running {inspect.currentframe().f_code.co_name}")
    model_yaml = _get_model_yaml()

    ModelYamlValidation(model_yaml).validate()
    CondaPacker(model_yaml).pack()
    if run_model_tests(_get_model_yaml_path()):
        ...
        #TODO: Pack & Publish

