import signal
import asyncio
import logging
from hypha.token_init import set_token
from hypha.service_registry import register_services
import inspect

def signal_break(signum, frame):
    logging.info(f"Received signal {signum}. Exiting...")
    exit(0)

async def main_loop():
    logging.info("main_loop()...")
    await register_services()

    while True:
        await asyncio.sleep(5)

def init_logging():
    log_format = "[%(asctime)s] [%(levelname)s] %(message)s"
    date_format = "%Y-%m-%d %H:%M:%S"
    logging.basicConfig(level=logging.INFO, format=log_format, datefmt=date_format)

def init() -> bool:
    init_logging()
    return set_token()

def local_test():
    print(f"Running {inspect.currentframe().f_code.co_name}")
    from test_conda_env import test_conda_env_creation
    test_conda_env_creation()

if __name__ == "__main__":
    local_test()
    #signal.signal(signal.SIGINT, signal_break)
    #if init():
    #    asyncio.run(main_loop())
