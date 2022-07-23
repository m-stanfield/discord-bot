import logging

import os
import yaml



class Logger:
    logger_initalized = False
    DEFAULT_DICT = {'path': 'settings/logging.yaml', 'level': None}
    inits = {}

    def __init__(self, name: str, init_dict: dict = {}):

        if not(self.logger_initalized):
            self._initLogger(init_dict)

        self.logger = logging.getLogger(name)

        self.info(f"Logger loaded in module {name}")

    @classmethod
    def _initLogger(cls, init_dict):
        import logging.config

        cls.inits = {**cls.DEFAULT_DICT, **init_dict}
        if not(os.path.isdir("logs")):
            os.mkdir("logs")

        if os.path.exists(cls.inits['path']):
            with open(cls.inits['path'], 'rt') as f:
                config = yaml.safe_load(f.read())
            if cls.inits['level'] is not None:
                for key in config['loggers']:
                    config['loggers'][key]['level'] = cls.inits['level'] or config['loggers'][key]['level']
            logging.config.dictConfig(config)
            cls.logger_initalized = True
        else:
            raise IOError(
                f"Logging configuration file does not exist. Expected file at location: {cls.inits['path']}")

    def info(self, msg, *args, **kwargs):
        self.logger.info(msg, *args, **kwargs)

    def debug(self, msg, *args, **kwargs):
        self.logger.debug(msg, *args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        self.logger.warning(msg, *args, **kwargs)

    def error(self, msg, *args, raiseError:Exception|None = None, **kwargs):
        self.logger.error(msg, *args, **kwargs)
        if isinstance(raiseError, Exception):
            raise raiseError

    def critical(self, msg, *args, **kwargs):
        self.logger.critical(msg, *args, **kwargs)

    def log(self, level, msg, *args, **kwargs):
        self.logger.log(level, msg, *args, **kwargs)


if __name__ == "__main__":
    def main():
        print(os.getcwd())

        logger = Logger(__name__)

        logger.info("Start reading Database")
        records = {"john": 55, "tom": 66}
        logger.debug("Records: %s", records)
        logger.info("Updating records ...")
        logger.info("Finish updating records")
        logger.error("Error Test")
        error = ValueError
        try:
            logger.error("Error Test", raiseError=error("Abcd"))
        except ValueError as err:
            print(f"Caught error: {err}")

    main()