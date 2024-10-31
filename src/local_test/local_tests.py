import inspect
import yaml
from pathlib import Path
from packing.conda_packer import CondaPacker
#from model_test import run_model_tests
from data.model_yaml_validation import ModelYamlValidation

def _get_model_yaml():
    model_yaml_file_path = Path(__file__).parent / "test_model.yml"
    with model_yaml_file_path.open('r') as file:
        return yaml.safe_load(file)

def test_services_locally():
    print(f"Running {inspect.currentframe().f_code.co_name}")
    model_yaml = _get_model_yaml()
    ModelYamlValidation(model_yaml).validate()
    CondaPacker(model_yaml).pack()

    #model_test_result = run_model_tests(model_yaml)
    #print(f"Model test result: {model_test_result}")

