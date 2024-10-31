from config import Config
from typing import Dict, Optional
from dataclasses import dataclass

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
    def _extract_weight_entry(model_yaml: Dict):
        weights_section = model_yaml.get("weights")
        if isinstance(weights_section, list) and weights_section:
            return weights_section[0]
        if isinstance(weights_section, dict) and weights_section:
            weight_entry_key, weight_entry = next(iter(weights_section.items()))
            weight_entry['format'] = weight_entry_key
            return weight_entry
        raise ValueError("Invalid weights format in YAML")  

    @staticmethod
    def _extract_name(model_yaml: Dict):
        return model_yaml.get("name", Config.UNKNOWN_NAME).replace(" ", "_")

    @classmethod
    def from_dict(cls, model_yaml: Dict) -> "ModelValues":
        name = cls._extract_name(model_yaml)
        weights = ModelWeights.from_dict(cls._extract_weight_entry(model_yaml))
        return cls(
            name=name,
            weights=weights
        )
