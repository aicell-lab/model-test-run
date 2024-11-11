import argparse
from packing.model_project import ModelProject
from typing import Tuple
from pathlib import Path
import yaml
from typing import Any
from data.model_yaml_validation import ModelYamlValidation
from packing.conda_packer import CondaPacker
from model_test import run_model_tests, print_model_test_result
from quick_validate import validate_rdf

def test_rdf_validity(project: ModelProject) -> bool:
    validation_result = validate_rdf(project.get_rdf_yaml_path())
    print(validation_result)
    if not validation_result.success:
        return False
    model_test_result = run_model_tests(project)
    print_model_test_result(model_test_result)
    if not model_test_result.success:
        return False
    return True

def run_tests(project: ModelProject) -> Tuple[bool, str]:
    if not test_rdf_validity(project):
        return False, "RDF yaml failed validation tests"
    return True, None

def pack_and_publish(project: ModelProject):
    #TODO: CondaPacker(project).pack()
    ...

def parse_args():
    parser = argparse.ArgumentParser(description="Run the script with a model URL.")
    parser.add_argument("--model", type=str, required=True, help="URL for the model.")
    return parser.parse_args()

def get_project_from_args():
    args = parse_args()
    model_url = args.model
    print(f"Testing [{model_url}]")
    project = ModelProject(model_url)
    print(f"zip [{project.download_path}], unpack [{project.project_path}]")
    return project

if __name__ == "__main__":
    """     from quick_test import validate
    with Path("/tmp/model_projects/hiding-tiger/rdf.yaml").open("r") as file:
        yaml_data = yaml.safe_load(file)
    from bioimageio.spec import validate_format, ValidationContext, build_description, load_description
    import yaml
    from pathlib import Path
    ctx = ValidationContext(perform_io_checks=False)
    with ctx:
        rd = build_description("/tmp/model_projects/hiding-tiger.zip")
    print(rd)
    available_weights = [value for _, value in rd.weights.model_dump().items() if value is not None]
    from packing.conda_env import get_conda_env, CondaEnv
    result = get_conda_env(entry=available_weights[0], env_name="test_name")
    print(result) """

    project = get_project_from_args()
    test_success, test_message = run_tests(project)
    if test_success:
        pack_and_publish(project)
    else:
        print(f"Error: {test_message}")

    

