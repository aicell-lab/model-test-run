import inspect
import yaml
from pathlib import Path
from model_test import run_model_tests
from data.model_yaml_validation import ModelYamlValidation
from packing.conda_packer import CondaPacker

def _get_model_yaml():
    model_yaml_file_path = Path(__file__).parent / "test_model.yml"
    with model_yaml_file_path.open('r') as file:
        return yaml.safe_load(file)

def _get_rdf_yaml():
    return 'https://uk1s3.embassy.ebi.ac.uk/public-datasets/bioimage.io/impartial-shrimp/1.1/files/rdf.yaml'

def test_services_locally():
    print(f"Running {inspect.currentframe().f_code.co_name}")
    model_yaml = _get_model_yaml()
    ModelYamlValidation(model_yaml).validate()
    CondaPacker(model_yaml).pack()
    if run_model_tests(_get_rdf_yaml()):
        ...
        #TODO: Pack & Publish

