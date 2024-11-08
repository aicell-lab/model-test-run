from bioimageio.core import test_model
from bioimageio.spec.summary import ValidationSummary
from packing.model_project import ModelProject

def _print_result(r: ValidationSummary):
    passed_details = [detail.name for detail in r.details if detail.status == 'passed']
    failed_details = [detail.name for detail in r.details if detail.status != 'passed']
    
    print(f"Model '{r.name}': {r.status}")
    
    if passed_details:
        print(f"{len(passed_details)} passed tests:")
        for name in passed_details:
            print(f"  {name}")
    
    if failed_details:
        print(f"{len(failed_details)} failed tests:")
        for name in failed_details:
            print(f"  {name}")

def run_model_tests(project: ModelProject) -> bool:
    result = test_model(source=project.get_rdf_yaml_path())
    _print_result(result)
    return result.status == 'passed'
