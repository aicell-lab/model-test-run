from bioimageio.spec.model import v0_5
from packing.conda_env import SupportedWeightsEntry
from config import Config
from typing import Dict
from data.model_values import ModelValues

class ModelYaml:
    FORMAT_TO_WEIGHTS_ENTRY = {
        "onnx": v0_5.OnnxWeightsDescr,
        "pytorch_state_dict": v0_5.PytorchStateDictWeightsDescr,
        "tensorflow_saved_model_bundle": v0_5.TensorflowSavedModelBundleWeightsDescr,
        "torchscript": v0_5.TorchscriptWeightsDescr,
    }

    def __init__(self, model_yaml: Dict):
        self.values = ModelValues.from_dict(model_yaml)

    def _check_weights(self):
        if not self.values.weights:
            raise ValueError("No weights found in the model YAML.")
        required_keys = ['source', 'opset_version', 'format']
        missing_keys = [key for key in required_keys if getattr(self.values.weights, key) is None]
        if missing_keys:
            raise ValueError(f"Weight entry must contain the following keys: {', '.join(missing_keys)}")

    def _check_weights_format(self):
        format = self.values.weights.format
        if format not in self.FORMAT_TO_WEIGHTS_ENTRY:
            raise ValueError(
                f"Unsupported format '{format}' found in weight entry. "
                f"Supported formats are: {', '.join(self.FORMAT_TO_WEIGHTS_ENTRY.keys())}"
            )
    
    def get_weights_source(self):
        return self.values.weights.source
        
    def get_weights_format(self):
        return self.values.weights.format
        
    def get_weights_descr_class(self):
        return ModelYaml.FORMAT_TO_WEIGHTS_ENTRY.get(self.get_weights_format())
    
    def get_name(self) -> str:
        return self.values.name

    def get_weights_descr(self) -> SupportedWeightsEntry:
        return self.get_weights_descr_class()(
            opset_version=self.values.weights.opset_version,
            source=self.values.weights.source
        )

    def validate(self):
        self._check_weights()
        self._check_weights_format()
    

