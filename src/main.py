import argparse
from packing.model_project import ModelProject
from typing import Tuple
from pathlib import Path
import yaml
from typing import Any
from data.model_yaml_validation import ModelYamlValidation
from packing.conda_packer import CondaPacker
from model_test import run_model_tests

def run_tests(project: ModelProject) -> Tuple[bool, str]:
    ModelYamlValidation(project.get_model_yaml()).validate()
    #CondaPacker(model_yaml).pack()

    if run_model_tests(project):
        return True, ""

    """try:
        model_yaml = load_yaml(project.get_rdf_yaml_path())
        ModelYamlValidation(model_yaml).validate()
        CondaPacker(model_yaml).pack()
        if run_model_tests(project):
            return True, ""
    except ValueError as e:
        return False, str(e) """
    #return False, "Model tests failed unexpectedly."

def parse_args():
    parser = argparse.ArgumentParser(description="Run the script with a model URL.")
    parser.add_argument("--model", type=str, required=True, help="URL for the model.")
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    model_url = args.model
    print(f"Testing [{model_url}]")
    project = ModelProject(model_url)
    print(f"zip [{project.download_path}], unpack [{project.project_path}]")

    run_tests(project)


