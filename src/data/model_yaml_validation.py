from typing import Dict
from data.model_values import ModelValues
from data.model_value_converter import ModelValueConverter

class ModelYamlValidation:
    def __init__(self, model_yaml: Dict):
        self.values = ModelValues.from_dict(model_yaml)

    def _check_weights(self):
        if not self.values.weights:
            raise ValueError("No weights found in the model YAML.")
        required_keys = ['source', 'version_number', 'version_type', 'format']

        for weight in self.values.weights:
            missing_keys = [key for key in required_keys if getattr(weight, key) is None]
            if missing_keys:
                raise ValueError(f"Weight entry must contain the following keys: {', '.join(missing_keys)}")

    def _check_weights_format(self):
        format = self.values.weights.format
        if format not in ModelValueConverter.FORMAT_TO_WEIGHTS_ENTRY:
            raise ValueError(
                f"Unsupported format '{format}' found in weight entry. "
                f"Supported formats are: {', '.join(ModelValueConverter.FORMAT_TO_WEIGHTS_ENTRY.keys())}"
            )

    def validate(self):
        self._check_weights()
        self._check_weights_format()
    

