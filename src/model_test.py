from bioimageio.core import test_model
from bioimageio.spec.summary import ValidationSummary

def _print_result(r: ValidationSummary):
    print(f"Model '{r.name}': {r.status}")
    for detail in r.details:
        print(f"{detail.name}: {detail.status}")

def run_model_tests(rdf_yaml_path) -> bool:
    result = test_model(source=rdf_yaml_path)
    _print_result(result)
    return result.status == 'passed'
