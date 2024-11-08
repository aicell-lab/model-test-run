import inspect
import yaml
from pathlib import Path
from model_test import run_model_tests
from data.model_yaml_validation import ModelYamlValidation
from packing.conda_packer import CondaPacker
import requests
from typing import Tuple

def _get_model_yaml_url():
    return "https://uk1s3.embassy.ebi.ac.uk/public-datasets/bioimage.io/chatty-frog/1/files/rdf.yaml"

def _yaml_from_url(url):
    response = requests.get(url)
    response.raise_for_status()
    return yaml.safe_load(response.text)

def run_tests(rdf_yaml_url) -> Tuple[bool, str]:
    try:
        model_yaml = _yaml_from_url(rdf_yaml_url)
        ModelYamlValidation(model_yaml).validate()
        CondaPacker(model_yaml).pack()
        if run_model_tests(rdf_yaml_url):
            return True, ""
    except ValueError as e:
        return False, str(e)
    return False, "Model tests failed unexpectedly."

def test_services_locally():
    print(f"Running {inspect.currentframe().f_code.co_name}")
    model_yaml_url = _get_model_yaml_url()
    
    result, msg = run_tests(model_yaml_url)
    if not result:
        print(f"Testing [{model_yaml_url}]: {msg}")
    else:
        print(f"Testing [{model_yaml_url}]: passed")


