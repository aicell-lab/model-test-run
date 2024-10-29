import yaml
from pathlib import Path
from conda_env import get_conda_env
from model_yaml import ModelYaml
import tempfile


def conda_pack_service(model_yaml: yaml):
    model_yaml_obj = ModelYaml(model_yaml)
    model_yaml_obj.validate()
    conda_env = get_conda_env(env_name=model_yaml_obj.get_name(), entry=model_yaml_obj.get_weights_descr())
    print(conda_env)


    