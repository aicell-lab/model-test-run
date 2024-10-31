from bioimageio.spec.model import v0_5
from packing.conda_env import SupportedWeightsEntry
from typing import Dict
from data.model_values import ModelValues

class ModelValueConverter:
    FORMAT_TO_WEIGHTS_ENTRY = {
        "onnx": v0_5.OnnxWeightsDescr,
        "pytorch_state_dict": v0_5.PytorchStateDictWeightsDescr,
        "tensorflow_saved_model_bundle": v0_5.TensorflowSavedModelBundleWeightsDescr,
        "torchscript": v0_5.TorchscriptWeightsDescr,
    }

    def __init__(self, model_yaml: Dict):
        self.values = ModelValues.from_dict(model_yaml)

    def get_weights_descr_class(self):
        return ModelValueConverter.FORMAT_TO_WEIGHTS_ENTRY.get(self.values.weights.format)

    def get_weights_descr(self) -> SupportedWeightsEntry:
        return self.get_weights_descr_class()(
            opset_version=self.values.weights.opset_version,
            source=self.values.weights.source
        )

    

