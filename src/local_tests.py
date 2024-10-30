import inspect
import yaml
from pathlib import Path
from packing.conda_packer import conda_pack_service
from model_test import run_model_tests
from model_yaml import ModelYaml

def _get_model_yaml():
    model_yaml_file_path = Path(__file__).parent / "test_model.yml"
    with model_yaml_file_path.open('r') as file:
        return yaml.safe_load(file)

def test_services_locally():
    print(f"Running {inspect.currentframe().f_code.co_name}")
    model_yaml = _get_model_yaml()
    ModelYaml(model_yaml).validate()
    conda_pack_service(model_yaml)
    #model_test_result = run_model_tests(model_yaml)
    #print(f"Model test result: {model_test_result}")

