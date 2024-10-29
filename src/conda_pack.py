import yaml
from conda_env import get_conda_env, CondaEnv
from model_yaml import ModelYaml
import subprocess
from config import Config

class CondaPack:
    def __init__(self, model_yaml: yaml):
        self.model_yaml = model_yaml
        self.model_yaml_obj = ModelYaml(model_yaml)
        self.model_yaml_obj.validate()
        self.conda_env = self._get_conda_env()
        self._set_paths()
    
    def _get_conda_env(self) -> CondaEnv:
        yaml_obj = self.model_yaml_obj
        return get_conda_env(env_name=yaml_obj.get_name(), entry=yaml_obj.get_weights_descr())  
    
    def _set_paths(self):
        yaml_obj = self.model_yaml_obj
        self.tmp_yaml_filepath = Config.Storage.tmp_dir / f"{yaml_obj.get_name()}.yml"
        self.tmp_conda_pack_filepath = Config.Storage.tmp_dir / f"{yaml_obj.get_name()}.tar.gz"
    
    def _dump_tmp_yaml(self):
        with open(self.tmp_yaml_filepath, 'w') as file:
            yaml.dump(self.model_yaml, file)

    def _run_conda_packing_script(self):
        process = subprocess.Popen(
            [Config.Scripts.conda_pack_path, str(self.tmp_yaml_filepath), str(self.tmp_conda_pack_filepath)],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        for line in process.stdout:
            print(line, end='')
        for line in process.stderr:
            print(line, end='')
        process.wait()

    def pack(self):
        self._dump_tmp_yaml()
        self._run_conda_packing_script()

def conda_pack_service(model_yaml: yaml):    
    CondaPack(model_yaml).pack()



    