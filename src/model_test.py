import yaml
from model_yaml import ModelYaml
from bioimageio.core import test_model
from bioimageio.spec.summary import ValidationSummary

def run_model_tests(model_yaml: yaml) -> ValidationSummary:
    my = ModelYaml(model_yaml)
    source = my.get_weights_source()
    weight_format = my.get_weights_format()
    return test_model(source=source, weight_format=weight_format)
