import logging
from testClass import testClass
from dotenv import load_dotenv
import os
import logging.config

import yaml

def setup_logging(
    path=None,
    level=None,
    env_key=None
):
    """Setup logging configuration

    """
    level = level or logging.INFO
    path = path or "logging.yaml"
    env_key = env_key or "LOG_CFG"
  #  path = default_path
    
    env_path = os.getenv(env_key, None)
    if env_path:
        path = env_path

    if os.path.exists(path):
        with open(path, 'rt') as f:
            config = yaml.safe_load(f.read())
        for key in config:
            print(f"{key}: {config[key]}")
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=level)



if __name__ == "__main__":
    load_dotenv()
    setup_logging() 

    logger = logging.getLogger()


    logger.info("Start reading Database")
    records = {"john": 55, "tom": 66}
    logger.debug("Records: %s", records)
    logger.info("Updating records ...")
    logger.info("Finish updating records")
    logger.error("Error Test")
    test = testClass()
