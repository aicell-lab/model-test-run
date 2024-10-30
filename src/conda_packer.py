import yaml
from conda_env import get_conda_env, CondaEnv
from model_yaml import ModelYaml
import subprocess
from config import Config
import conda_pack

class CondaPacker:
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

    def _remove_conda_env_from_yaml(self):
        env_name = self.model_yaml_obj.get_name()
        print(f"Removing existing conda environment '{env_name}' if it exists...")
        try:
            subprocess.run(
                ["conda", "env", "remove", "--name", env_name, "--yes"],
                check=True
            )
            print(f"Removed existing conda environment '{env_name}'.")
        except subprocess.CalledProcessError:
            print(f"No existing environment '{env_name}' found. Proceeding to create a new one.")

    def _create_conda_env_from_yaml(self):
            env_name = self.model_yaml_obj.get_name()
            print(f"Creating conda environment from {self.tmp_yaml_filepath}...")
            subprocess.run(
                ["conda", "env", "create", "-f", str(self.tmp_yaml_filepath), "-n", env_name],
                check=True
            )

    def pack(self):
        self._dump_tmp_yaml()

        self._remove_conda_env_from_yaml()
        self._create_conda_env_from_yaml()

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

        self._remove_conda_env_from_yaml()
        print(f"Packing done. Output saved to {out_path}.")

def conda_pack_service(model_yaml: yaml):    
    CondaPacker(model_yaml).pack()



    