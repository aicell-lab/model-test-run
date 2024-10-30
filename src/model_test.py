import inspect
import yaml
from pathlib import Path
from conda_pack import conda_pack_service
from model_yaml import ModelYaml
from bioimageio.core import test_model
from bioimageio.spec.summary import ValidationSummary

def run_model_tests(model_yaml: yaml) -> ValidationSummary:
    model_yaml_obj = ModelYaml(model_yaml)
    ...