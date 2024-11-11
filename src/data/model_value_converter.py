from bioimageio.spec.model import v0_5
from packing.conda_env import SupportedWeightsEntry
from typing import Dict, List
from data.model_values import ModelValues, ModelWeights
from pydantic import HttpUrl
from bioimageio.spec import load_description

class ModelValueConverter:
    FORMAT_TO_WEIGHTS_ENTRY = {
        "onnx": v0_5.OnnxWeightsDescr,
        "pytorch_state_dict": v0_5.PytorchStateDictWeightsDescr,
        "tensorflow_saved_model_bundle": v0_5.TensorflowSavedModelBundleWeightsDescr,
        "torchscript": v0_5.TorchscriptWeightsDescr,
    }

    def __init__(self, model_yaml: Dict):
        self.values = ModelValues.from_dict(model_yaml)
        self.w_index = 0 # Currently only tests the 1st weight entry

    def _get_weight_sources(self) -> List[str]:
        return [weight.source for weight in self.values.weights]
    
    def _get_weight(self) -> ModelWeights:
        return self.values.weights[self.w_index]

    def get_weights_descr_class(self):
        return ModelValueConverter.FORMAT_TO_WEIGHTS_ENTRY.get(self._get_weight().format)

    def get_weights_descr(self) -> SupportedWeightsEntry:
        weight = self._get_weight()
        version_info = {
            weight.version_type: weight.version_number
        }
        return self.get_weights_descr_class()(
            **version_info,
            source=self._get_weight_source_urls()[self.w_index]
        )

    

