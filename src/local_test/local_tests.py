import inspect
from local_test.dataset_id_test import run_tests

def _get_model_yaml_url():
    return "https://uk1s3.embassy.ebi.ac.uk/public-datasets/bioimage.io/chatty-frog/1/files/rdf.yaml"

def test_services_locally():
    print(f"Running {inspect.currentframe().f_code.co_name}")
    model_yaml_url = _get_model_yaml_url()
    
    result, msg = run_tests(model_yaml_url)
    if not result:
        print(f"Testing [{model_yaml_url}]: {msg}")
    else:
        print(f"Testing [{model_yaml_url}]: passed")


