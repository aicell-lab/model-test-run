import inspect
import yaml
from pathlib import Path
from model_test import run_model_tests
from data.model_yaml_validation import ModelYamlValidation
from packing.conda_packer import CondaPacker
import requests

def _get_model_yaml_url():
    record_id = "6647688"
    return f"https://zenodo.org/records/{record_id}/files/rdf.yaml"

def _yaml_from_url(url):
    response = requests.get(url)
    response.raise_for_status()
    return yaml.safe_load(response.text)

# Have function that tests everything and returns result and optional error message.

def test_services_locally():
    print(f"Running {inspect.currentframe().f_code.co_name}")

    model_yaml_url = _get_model_yaml_url()
    model_yaml = _yaml_from_url(model_yaml_url)

    ModelYamlValidation(model_yaml).validate()
    CondaPacker(model_yaml).pack()
    if run_model_tests(model_yaml_url):
        ...
        #TODO: Pack & Publish

