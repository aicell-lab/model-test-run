import signal
import asyncio
import logging
from hypha.token_init import set_token
from hypha.service_registry import register_services
import inspect
import argparse
from packing.model_project import ModelProject

def signal_break(signum, frame):
    logging.info(f"Received signal {signum}. Exiting...")
    exit(0)

def init_logging():
    log_format = "[%(asctime)s] [%(levelname)s] %(message)s"
    date_format = "%Y-%m-%d %H:%M:%S"
    logging.basicConfig(level=logging.INFO, format=log_format, datefmt=date_format)

def init() -> bool:
    init_logging()
    return set_token()

async def main_loop():
    logging.info("main_loop()...")
    await register_services()
    while True:
        await asyncio.sleep(5)

def start():
    signal.signal(signal.SIGINT, signal_break)
    if init():
        asyncio.run(main_loop())

def local_test():
    print(f"Running {inspect.currentframe().f_code.co_name}")
    from local_test.dataset_id_retrieval import get_dataset_ids
    from local_test.dataset_id_test import test_dataset_id
    for dataset_id in get_dataset_ids():
        print(test_dataset_id(dataset_id))

def parse_args():
    parser = argparse.ArgumentParser(description="Run the script with a model URL.")
    parser.add_argument("--model", type=str, required=True, help="URL for the model.")
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    model_url = args.model
    print(f"Testing [{model_url}]...")
    project = ModelProject(model_url)
    print(project.download_path)

    #local_test()
    #start()
