import requests
from typing import List, Dict

#Formatting hints for retrieving data using zenodo urls:
##https://zenodo.org/records/<record_id> OR <dataset_id>/files/rdf.yaml
##Example id entry from json: {"id": "10.5281/zenodo.5869899"}
##id format: "<DOI>/zenodo.<dataset_id>/<record_id>"
##dataset_id is the original project version and record_id marks an update, normally the latest update

bioengine_json_url = "https://raw.githubusercontent.com/bioimage-io/bioengine-model-runner/gh-pages/manifest.bioengine.json"

def _download_json_as_dict(url: str) -> Dict:
    response = requests.get(url)
    response.raise_for_status()
    return response.json()  

def _extract_dataset_ids(json_data: Dict) -> List[str]:
    dataset_ids = []
    for entry in json_data.get("collection", []):
        if "zenodo." in entry["id"]:
            dataset_id = entry["id"].split("zenodo.")[1]
            dataset_ids.append(dataset_id)
    return dataset_ids

def get_dataset_ids() -> List[str]:
    return _extract_dataset_ids(_download_json_as_dict(bioengine_json_url))