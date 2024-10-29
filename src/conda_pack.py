import yaml
from pathlib import Path
from conda_env import get_conda_env, CondaEnv
from model_yaml import ModelYaml
import tempfile
import subprocess
from config import Config

def _get_conda_env(model_yaml: yaml) -> CondaEnv:
    model_yaml_obj = ModelYaml(model_yaml)
    model_yaml_obj.validate()
    conda_env = get_conda_env(env_name=model_yaml_obj.get_name(), entry=model_yaml_obj.get_weights_descr())  
    return conda_env

def conda_pack_service(model_yaml: yaml):
    conda_env = _get_conda_env(model_yaml)  
    print(conda_env)

    model_yaml_obj = ModelYaml(model_yaml)
    tmp_yaml_filepath = Config.Storage.tmp_dir / f"{model_yaml_obj.get_name()}.yml"
    tmp_conda_pack_filepath = Config.Storage.tmp_dir / f"{model_yaml_obj.get_name()}.tar.gz"
    
    with open(tmp_yaml_filepath, 'w') as file:
        yaml.dump(model_yaml, file)

    result = subprocess.run([Config.Scripts.conda_pack_path, str(tmp_yaml_filepath), str(tmp_conda_pack_filepath)], capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error in running script:\n{result.stderr}")
        raise RuntimeError("Failed to execute conda environment packaging script.")
    print("........")
    print(result.stdout)

    #tmp_path = Path(tempfile.gettempdir())
    #print(tmp_path)


    