import yaml
from model_yaml import ModelYaml
from config import Config
import conda_pack
from typing import Dict

class CondaPacker:
    def __init__(self, model_yaml: Dict):
        self.model_yaml_obj = ModelYaml(model_yaml)
        self.model_yaml_obj.validate()
        self.tmp_conda_pack_filepath = Config.Storage.tmp_dir / f"{self.model_yaml_obj.get_name()}.tar.gz"

    def store_conda_pack(self):
        env_name = self.model_yaml_obj.get_name()
        print(f"Packing environment: {env_name}...")
        out_path = conda_pack.pack(
            name=env_name,
            output=str(self.tmp_conda_pack_filepath),
            format="tar.gz",
            verbose=True,
            force=True,
            n_threads=-1
        )
        print(f"Packing done. Output saved to {out_path}.")

    def pack(self):
        self.model_yaml_obj.remove_conda_env()
        self.model_yaml_obj.create_conda_env()
        self.model_yaml_obj.install_dependencies()
        self.store_conda_pack()
        self.model_yaml_obj.remove_conda_env()

def conda_pack_service(model_yaml: yaml):    
    CondaPacker(model_yaml).pack()



    