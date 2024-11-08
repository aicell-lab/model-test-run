import yaml
from model_test import run_model_tests
from data.model_yaml_validation import ModelYamlValidation
from packing.conda_packer import CondaPacker
import requests
from typing import Tuple, List
from pydantic import HttpUrl


def _get_redirected_url(url: HttpUrl) -> HttpUrl:
    """Helper function to get the final URL after redirection."""
    response = requests.get(url, allow_redirects=True)
    response.raise_for_status()
    return response.url

def _get_zenodo_project_url(dataset_id: str) -> HttpUrl:
    project_url = f"https://zenodo.org/records/{dataset_id}"
    return _get_redirected_url(project_url)

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

def _rdf_url_from_dataset_id(dataset_id: str) -> HttpUrl:
    return f"{_get_zenodo_project_url(dataset_id)}/files/rdf.yaml"

def test_dataset_id(dataset_id: str) -> Tuple[bool, str]:
    return run_tests(_rdf_url_from_dataset_id(dataset_id))

def test_dataset_ids(dataset_ids: List[str]) -> List[Tuple[bool, str]]:
    return [test_dataset_id(dataset_id) for dataset_id in dataset_ids]




