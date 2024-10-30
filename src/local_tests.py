import inspect
import yaml
from pathlib import Path
from conda_pack import conda_pack_service
from model_test import run_model_tests

def _get_model_yaml():
    model_yaml_file_path = Path(__file__).parent / "test_model.yml"
    with model_yaml_file_path.open('r') as file:
        return yaml.safe_load(file)

def test_services_locally():
    print(f"Running {inspect.currentframe().f_code.co_name}")
    conda_pack_service(_get_model_yaml())
    model_test_result = run_model_tests(_get_model_yaml())
    print(f"Model test result: {model_test_result}")

