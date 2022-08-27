from __future__ import annotations
import argparse
import dotenv
import os
import yaml
from yaml.loader import SafeLoader
from src.logger import Logger
import logging

logger = Logger(__name__)
ENV_KEYS = ["DISCORD_TOKEN", "SQLITE_DB_FILE","SQLITE_DB_PATH", "BOT_NAMES",
            "timeout_duration", "timeout_interval"]

class Settings:
    settings: dict = None

    def __init__(self):
        if not(self.settings):       
            logger.debug("Initializaing settings")
            self._initializeSettings()
            self._load_env()
            self._parseArgs()
            self._loadDataYaml()
            self.log()

    @classmethod
    def _initializeSettings(cls):
        cls.settings = {}


    def __repr__(self) -> str:
        output = str(self)
        for i, (key, item) in enumerate(self.settings.items()):
            output += f"\n\t{self._key2Str(key)}: {str(item)}"
        return output

    def __str__(self) -> str:
        output = ""
        for i, key in enumerate(self.settings):
            if i > 0:
                output += "\n"
            output += self._key2Str(key)
        return output

    @classmethod
    def init(cls):
        return Settings()

    @classmethod
    def get(cls, keys: str|list):
        result = None
        if type(keys) is list:
            result = cls.getSettings()
            for key in keys:
                result = result[key]
        else:
            result = cls.settings[keys] if keys in cls.settings else None
        return result

    @classmethod
    def getSettings(cls):
        return dict(cls.settings)

    @classmethod
    def getKeys(cls):
        return cls.settings.keys()

    @classmethod
    def keys(cls):
        return cls.getKeys()

    @classmethod
    def _key2Str(cls, key: str) -> str:
        output: str
        if key.endswith("TOKEN"):
            output = f"{key}: REDACTED"
        elif key == "DATA_BASE":
            output = f"{key} Tables: {cls.settings[key].keys()}"
        else:
            output = f"{key}: {cls.settings[key]}"
        return output

    @classmethod
    def log(cls, level=logging.DEBUG):
        logger.log(level=level, msg="Logging discord bot initilization settings")
        key: str
        for key in cls.settings:
            logger.log(level=level, msg=cls._key2Str(key))

    @classmethod
    def _load_env(cls):
        dotenv.load_dotenv()

        for key in ENV_KEYS:
            try:
                cls.settings[key] = os.getenv(key)
            except KeyError:
                logger.error(f"Invalid enrivoment key on load: {key}")

    @classmethod
    def _parseArgs(cls):
        parser = argparse.ArgumentParser(
            description="Sets runtime settings for discord bot")
        parser.add_argument('--TEST_MODE', type=int, default=0)
        parser.add_argument('--UPDATE_ALL', type=int, default=1)
        parser.add_argument('--DISABLE_WAKEUP', type=int, default=0)
        parser.add_argument('--TEST_LOAD', type=int, default=0)
        parser.add_argument('--LOG', type=int, default=None)
        args = parser.parse_args()

        for key in vars(args):
            cls.settings[key] = vars(args)[key]

    @classmethod
    def _loadDataYaml(cls):
        def get_dirs(input_dict:dict) -> str:
            for key, value in input_dict.items():
                if isinstance(value, dict):
                    for val in get_dirs(value):
                        yield val
                else:
                    yield value

        with open('settings/data.yaml') as f:
            a = yaml.load(f, Loader=SafeLoader)
        cls.settings['data'] = a
        for directory in get_dirs(cls.settings['data']):
            if not(os.path.isdir(directory)):
                os.makedirs(directory)


        

Settings.init()


if __name__ == "__main__":
    def main():
        Settings.init()
        settings1 = Settings()
        settings2 = Settings()
        print(settings1)
        print(settings1.get(['data','images','sticker']))
    main()

