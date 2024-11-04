from bioimageio.spec.model import v0_5
from packing.conda_env import SupportedWeightsEntry
from typing import Dict
from data.model_values import ModelValues
from data.record_files import RecordFileHandler

class ModelValueConverter:
    FORMAT_TO_WEIGHTS_ENTRY = {
        "onnx": v0_5.OnnxWeightsDescr,
        "pytorch_state_dict": v0_5.PytorchStateDictWeightsDescr,
        "tensorflow_saved_model_bundle": v0_5.TensorflowSavedModelBundleWeightsDescr,
        "torchscript": v0_5.TorchscriptWeightsDescr,
    }

    def __init__(self, model_yaml: Dict):
        self.values = ModelValues.from_dict(model_yaml)
        self.record_files_handler = RecordFileHandler(model_yaml)
        self.record_files_handler.download_and_extract_files()

    def get_weights_descr_class(self):
        return ModelValueConverter.FORMAT_TO_WEIGHTS_ENTRY.get(self.values.weights.format)

    def get_weights_descr(self) -> SupportedWeightsEntry:
        version_info = {
            self.values.weights.version_type: self.values.weights.version_number
        }
        return self.get_weights_descr_class()(
            **version_info,
            source=self.record_files_handler.get_weights_source_path()
        )

    

