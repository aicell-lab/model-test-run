import yaml
from model_yaml import ModelYaml
from bioimageio.core import test_model
from bioimageio.spec.summary import ValidationSummary
from model_download import ModelDownloader

def run_model_tests(model_yaml: yaml) -> ValidationSummary:
    my = ModelYaml(model_yaml)
    source = my.get_weights_source()
    weight_format = my.get_weights_format()

    downloader = ModelDownloader(source)
    downloader.download_model()
    model_filepath = str(downloader.get_download_filepath())

    return test_model(source=model_filepath, weight_format=weight_format)
