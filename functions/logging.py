import logging

from dotenv import load_dotenv
import os
import logging.config

import yaml

def setup_logging(
    path:str=None,
    mode:int=None,
    env_key:str=None
):
    """Setup logging configuration

    """
    mode_dict = {0:"INFO",1:"DEBUG"}
    level = mode_dict[0] if mode not in mode_dict else mode_dict[mode]
    
    path = path or "logging.yaml"
    env_key = env_key or "LOG_CFG"
  #  path = default_path
    
    env_path = os.getenv(env_key, None)
    if env_path:
        path = env_path

    if os.path.exists(path):
        with open(path, 'rt') as f:
            config = yaml.safe_load(f.read())

    
        for key in config["loggers"]:
            config['loggers'][key]['level'] = level
        logging.config.dictConfig(config)
    else:
        raise IOError(f"Logging configuration file does not exist. Expected file at location: {path}")
    


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
