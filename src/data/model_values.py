from config import Config
from typing import Dict, Optional, Any, List
from dataclasses import dataclass
import re

@dataclass(frozen=True)
class ModelWeightArchitecture:
    callable: str
    kwargs: Optional[Dict[str, Any]]
    sha256: Optional[str] = None
    
    @classmethod
    def from_dict(cls, architecture_data: Dict) -> "ModelWeightArchitecture":
        return cls(
            callable=architecture_data.get("callable"),
            kwargs=architecture_data.get("kwargs"),
            sha256=architecture_data.get("sha256")
        )

@dataclass(frozen=True)
class ModelWeights:
    source: str
    version_number: int
    version_type: str
    format: str
    architecture: Optional[ModelWeightArchitecture] = None

    @classmethod
    def from_dict(cls, weight_entry: Dict) -> "ModelWeights":
        format_name, format_data = next(iter(weight_entry.items()))

        architecture = (
            ModelWeightArchitecture.from_dict(format_data["architecture"])
            if "architecture" in format_data else None
        )
        
        return cls(
            source=format_data.get("source"),
            version_number=ModelWeights._extract_version_number(format_data),
            version_type=ModelWeights._extract_version_type(format_data),
            format=format_name,
            architecture=architecture
        )
    
    @staticmethod
    def _extract_version_number(format_data: Dict) -> int:
        version_key = next((k for k in format_data if "version" in k), None)
        return format_data.get(version_key) if version_key else None

    @staticmethod
    def _extract_version_type(format_data: Dict) -> str:
        return next((k for k in format_data if "version" in k), None)
    
@dataclass(frozen=True)
class ModelZenodo:
    doi_prefix: str
    dataset_id: str
    revision_id: Optional[str]

    @classmethod
    def from_dict(cls, config_entry: Dict) -> "ModelZenodo":
        config_id = ModelZenodo._extract_zenodo_id(config_entry)
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
    weights: List[ModelWeights]
    zenodo: Optional[ModelZenodo]

    @staticmethod
    def _extract_name(model_yaml: Dict):
        return model_yaml.get("name", Config.UNKNOWN_NAME).replace(" ", "_")

    @classmethod
    def from_dict(cls, model_yaml: Dict) -> "ModelValues":
        name = cls._extract_name(model_yaml)
        weights = [
            ModelWeights.from_dict({format_name: format_data})
            for format_name, format_data in model_yaml.get("weights").items()
        ]
        zenodo = ModelZenodo.from_dict(model_yaml.get("id") or model_yaml.get("config"))
        return cls(
            name=name,
            weights=weights,
            zenodo=zenodo
        )
