bioengine_json_url = "https://raw.githubusercontent.com/bioimage-io/bioengine-model-runner/gh-pages/manifest.bioengine.json"

#str formatting hints:
##https://zenodo.org/records/<record_id>/files/rdf.yaml
##Example id: {"id": "10.5281/zenodo.5869899"}
##id format: "<DOI (Digital Object Identifier)>/zenodo.<record_id>"

### TODO: 
# Download json_url
# Extract all record_ids in a list
# Convert list to list of urls pointing to rdf.yaml
# Add code that can convert an url to a local yaml object
# Add code that can create ModelValues from yaml url
# for each local yaml object + url
#   run_tests(yaml)