from bioimageio.core import test_model
from bioimageio.spec.summary import ValidationSummary

def _print_result(r: ValidationSummary):
    passed_details = []
    failed_details = []
    
    for detail in r.details:
        if detail.status == 'passed':
            passed_details.append(detail.name)
        else:
            failed_details.append(detail.name)
    
    print(f"Model '{r.name}': {r.status}")
    print("passed:")
    for name in passed_details:
        print(f"  {name}")
    print("failed:")
    for name in failed_details:
        print(f"  {name}")

def run_model_tests(rdf_yaml_path) -> bool:
    result = test_model(source=rdf_yaml_path)
    _print_result(result)
    return result.status == 'passed'
