from data.model_values import ModelValues
import conda_pack
from typing import Dict
from packing.conda_env_controller import CondaEnvController
from packing.conda_file_handler import CondaFileHandler

class CondaPacker:
    def __init__(self, model_yaml: Dict):
        self.values = ModelValues.from_dict(model_yaml)
        self.env_controller = CondaEnvController(model_yaml)
        self.file_handler = CondaFileHandler(model_yaml)

    def _conda_pack(self) -> str:
        return conda_pack.pack(
            name=self.values.name,
            output=str(self.file_handler.get_conda_pack_path()),
            format="tar.gz",
            verbose=True,
            force=True,
            n_threads=-1
        )

    def store_conda_pack(self):
        print(f"Packing environment: {self.values.name}...")
        print(f"Packing done. Output saved to {self._conda_pack()}.")

    def _setup_conda_env(self):
        self.env_controller.remove_conda_env()
        self.env_controller.create_conda_env()
        self.env_controller.install_dependencies()

    def pack(self):
        self._setup_conda_env()
        self.store_conda_pack()
        self.env_controller.remove_conda_env()




    