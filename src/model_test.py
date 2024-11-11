#from bioimageio.spec.summary import ValidationSummary
from bioimageio.core import test_model
from packing.model_project import ModelProject
from dataclasses import dataclass
from typing import List

@dataclass
class ModelTestResult:
    success: bool
    passed_details: List[str]
    failed_details: List[str]

def print_model_test_result(result: ModelTestResult):
    status = "passed" if result.success else "failed"
    print(f"Model Test Result: {status}")
    if result.passed_details:
        print(f"{len(result.passed_details)} passed tests:")
        for name in result.passed_details:
            print(f"  {name}")
    if result.failed_details:
        print(f"{len(result.failed_details)} failed tests:")
        for name in result.failed_details:
            print(f"  {name}")

def run_model_tests(project: ModelProject) -> ModelTestResult:
    result = test_model(source=project.get_rdf_yaml_path())
    passed_details = [detail.name for detail in result.details if detail.status == 'passed']
    failed_details = [detail.name for detail in result.details if detail.status != 'passed']
    
    return ModelTestResult(
        success=result.status == 'passed',
        passed_details=passed_details,
        failed_details=failed_details
    )
