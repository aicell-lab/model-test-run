from config import Config
from typing import Dict, Optional, Type
from dataclasses import dataclass, field

@dataclass(frozen=True)
class ModelWeights:
    source: str
    opset_version: Optional[int]
    format: str

    @classmethod
    def from_dict(cls, weight_entry: Dict) -> "ModelWeights":
        return cls(
            source=weight_entry.get("source"),
            opset_version=weight_entry.get("opset_version"),
            format=weight_entry.get("format")
        )

@dataclass(frozen=True)
class ModelValues:
    name: str
    weights: ModelWeights

    @staticmethod
    def _get_weight_entry(model_yaml: Dict):
        weights_section = model_yaml.get("weights")
        if isinstance(weights_section, list) and weights_section:
            return weights_section[0]
        if isinstance(weights_section, dict) and weights_section:
            weight_entry_key, weight_entry = next(iter(weights_section.items()))
            weight_entry['format'] = weight_entry_key
            return weight_entry
        raise ValueError("Invalid weights format in YAML")  

    @classmethod
    def from_dict(cls, model_yaml: Dict) -> "ModelValues":
        name = model_yaml.get("name", Config.UNKNOWN_NAME).replace(" ", "_")
        weight_entry = cls._get_weight_entry(model_yaml)
        return cls(
            name=name,
            weights=ModelWeights.from_dict(weight_entry)
        )
