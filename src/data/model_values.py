from config import Config
from typing import Dict, Optional, Any
from dataclasses import dataclass
import re

@dataclass(frozen=True)
class ModelWeights:
    source: str
    version_number: int
    version_type: str
    format: str

    @classmethod
    def from_dict(cls, weight_entry: Dict) -> "ModelWeights":
        return cls(
            source=weight_entry.get("source"),
            version_number=ModelWeights._extract_version_number(weight_entry),
            version_type=ModelWeights._extract_version_type(weight_entry),
            format=weight_entry.get("format")
        )
    
    @staticmethod
    def _extract_version_number(weight_entry: Dict) -> int:
        version_key = next((k for k in weight_entry if "version" in k), None)
        return weight_entry.get(version_key) if version_key else None

    @staticmethod
    def _extract_version_type(weight_entry: Dict) -> str:
        return next((k for k in weight_entry if "version" in k), None)
    
@dataclass(frozen=True)
class ModelZenodo:
    doi_prefix: str
    dataset_id: str
    revision_id: Optional[str]

    @classmethod
    def from_dict(cls, model_yaml: Dict) -> "ModelZenodo":
        config_id = ModelZenodo._extract_config_id(model_yaml)
        if config_id:
            parts = config_id.split('/')
            if len(parts) == 3:  # format: "10.xxx/zenodo.yyyy/revision"
                doi_prefix = parts[0]
                dataset_part = parts[1]
                revision_id = parts[2]
            elif len(parts) == 2:  # format: "10.xxx/zenodo.yyyy"
                doi_prefix = parts[0]
                dataset_part = parts[1]
                revision_id = None
            else:
                raise ValueError(f"Expected config_id format 'prefix/dataset_id' or 'prefix/dataset_id/revision_id', got '{config_id}'")
            dataset_id = dataset_part.split("zenodo.")[-1] if "zenodo." in dataset_part else dataset_part
            return cls(
                doi_prefix=doi_prefix,
                dataset_id=dataset_id,
                revision_id=revision_id
            )
        else:
            raise ValueError("No config_id found in the provided model_yaml.")
    
    @staticmethod
    def _extract_config_id(model_yaml: Dict) -> Optional[str]:
        return ModelZenodo._extract_zenodo_id(model_yaml.get("config", {}))
    
    @staticmethod
    def _extract_zenodo_id(model_yaml: Dict) -> Optional[str]:
        zenodo_pattern = re.compile(r"10\.\d+/zenodo\.\d+(/\d+)?")
        def search_zenodo_id(data: Any) -> Optional[str]:
            if isinstance(data, dict):
                for _, value in data.items():
                    result = search_zenodo_id(value)
                    if result:
                        return result
            elif isinstance(data, list):
                for item in data:
                    result = search_zenodo_id(item)
                    if result:
                        return result
            elif isinstance(data, str):
                if zenodo_pattern.match(data):
                    return data
        return search_zenodo_id(model_yaml)
 
@dataclass(frozen=True)
class ModelValues:
    name: str
    weights: ModelWeights
    zenodo: ModelZenodo

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
        zenodo = ModelZenodo.from_dict(model_yaml)
        return cls(
            name=name,
            weights=weights,
            zenodo=zenodo
        )
