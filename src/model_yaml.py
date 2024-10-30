from bioimageio.spec.model import v0_5
from packing.conda_env import SupportedWeightsEntry
from config import Config
from typing import Dict

class ModelYaml:
    FORMAT_TO_WEIGHTS_ENTRY = {
        "onnx": v0_5.OnnxWeightsDescr,
        "pytorch_state_dict": v0_5.PytorchStateDictWeightsDescr,
        "tensorflow_saved_model_bundle": v0_5.TensorflowSavedModelBundleWeightsDescr,
        "torchscript": v0_5.TorchscriptWeightsDescr,
    }

    def __init__(self, model_yaml: Dict):
        self.model_yaml = model_yaml

    def _check_weights(self):
        if not self.model_yaml.get('weights'):
            raise ValueError("No weights found in the model YAML.")
        
        required_keys = ['source', 'opset_version', 'format']
        missing_keys = [key for key in required_keys if key not in self._get_weights_entry()]
        if missing_keys:
            raise ValueError(f"Weight entry must contain the following keys: {', '.join(missing_keys)}")

    def _check_weights_format(self):
        weight_entry = self.model_yaml['weights'][0]
        if weight_entry['format'] not in self.FORMAT_TO_WEIGHTS_ENTRY:
            raise ValueError(
                f"Unsupported format '{weight_entry['format']}' found in weight entry. "
                f"Supported formats are: {', '.join(self.FORMAT_TO_WEIGHTS_ENTRY.keys())}"
            )
        
    def _get_weights_entry(self):
        return self.model_yaml['weights'][0]
    
    def _get_weights_opset_version(self):
        return self._get_weights_entry().get("opset_version")
    
    def get_weights_source(self):
        return self._get_weights_entry().get("source")
        
    def get_weights_format(self):
        return self._get_weights_entry()['format']
        
    def get_weights_descr_class(self):
        return ModelYaml.FORMAT_TO_WEIGHTS_ENTRY.get(self.get_weights_format())
    
    def get_name(self) -> str:
        return self.model_yaml.get("name").replace(" ", "_") or Config.UNKNOWN_NAME

    def get_weights_descr(self) -> SupportedWeightsEntry:
        return self.get_weights_descr_class()(
            opset_version=self._get_weights_opset_version(),
            source=self.get_weights_source()
        )

    def validate(self):
        self._check_weights()
        self._check_weights_format()
    

