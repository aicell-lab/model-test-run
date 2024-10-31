import yaml
from data.model_values import ModelValues
from config import Config
import conda_pack
from typing import Dict
from packing.conda_env_controller import CondaEnvController

class CondaPacker:
    def __init__(self, model_yaml: Dict):
        self.values = ModelValues.from_dict(model_yaml)
        self.env_controller = CondaEnvController(model_yaml)

    def _get_conda_pack_filepath(self):
        return Config.Storage.tmp_dir / f"{self.values.name}.tar.gz"

    def store_conda_pack(self):
        print(f"Packing environment: {self.values.name}...")
        out_path = conda_pack.pack(
            name=self.values.name,
            output=str(self._get_conda_pack_filepath()),
            format="tar.gz",
            verbose=True,
            force=True,
            n_threads=-1
        )
        print(f"Packing done. Output saved to {out_path}.")

    def _setup_conda_env(self):
        self.env_controller.remove_conda_env()
        self.env_controller.create_conda_env()
        self.env_controller.install_dependencies()

    def pack(self):
        self._setup_conda_env()
        self.store_conda_pack()
        self.env_controller.remove_conda_env()

def conda_pack_service(model_yaml: yaml):    
    CondaPacker(model_yaml).pack()



    