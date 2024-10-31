import yaml
from src.data.model_yaml_validation import ModelYaml
from bioimageio.core import test_model
from bioimageio.spec.summary import ValidationSummary
from model_download import ModelDownloader

def run_model_tests(model_yaml: yaml) -> ValidationSummary:
    my = ModelYaml(model_yaml)
    source = my.get_weights_source()
    weight_format = my.get_weights_format()

    tmp_path = '/tmp/nucleisegmentationboundarymodel_onnx/weights.onnx'

    return test_model(source=tmp_path, weight_format=weight_format)
