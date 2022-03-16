import argparse
import dotenv
import os

from src.logging.logger import Logger
import logging

logger = Logger(__name__)
ENV_KEYS = ["DISCORD_TOKEN", "SQLITE_DB", "BOT_NAME",
            "timeout_duration", "timeout_interval"]


class Settings:
    settings: dict | None = None

    def __init__(self):
        self.init()

    def __str__(self):
        output = ""
        for i, key in enumerate(self.settings):
            if i > 0:
                output += "\n"
            output += self._key2Str(key)
        return output

    @classmethod
    def init(cls):
        logger.info("init")

        if cls.settings is None:
            logger.debug("Initializaing settings")
            cls.settings = {}
            cls._load_env()
            cls._parseArgs()
            cls._loadSchema()
            cls.log()

    @classmethod
    def get(cls, key: str):
        return cls.settings[key]

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
    def _loadSchema(cls):
        iniName = ['guild_defaults', 'user_defaults']
        iniExtension = '.ini'
        iniPath = 'settings/database/'
        if not(os.path.isdir(iniPath)):
            errmsg = "Directory {iniPath} does not exist for the database initialization settings"
            logger.error(errmsg)
            raise FileNotFoundError(errmsg)
        db_dic = {}
        for fileName in iniName:
            path = iniPath + fileName + iniExtension
            if os.path.exists(path):
                with open(path, 'r') as f:
                    content = f.readlines()

                content = [x.strip().replace('\t', '').replace(' ', '')
                           for x in content]
                dic = {}
                for line in content:
                    if len(line) > 0:
                        a = line.split('=')
                        varname = a[0]
                        vartype = a[1].split(':')[0]
                        varval = a[1].split(':')[1]

                        if vartype == 'BOOL':
                            dic[a[0]] = ('BOOL', bool(int(varval)))
                        elif vartype == 'TEXT':
                            dic[a[0]] = ('TEXT', varval.replace('"', "'"))
                        elif vartype == 'FLOAT':
                            dic[a[0]] = ('FLOAT', float(varval))
                        elif vartype == 'BIGINT':
                            dic[a[0]] = ('BIGINT', int(varval))
                        else:
                            try:
                                dic[a[0]] = ('BIGINT', int(varval))
                            except ValueError:
                                dic[a[0]] = ('TEXT', str(varval))
                db_dic[f'{fileName}'.replace('_defaults', "").upper()] = dic

        cls.settings['DATA_BASE'] = db_dic


if __name__ == "__main__":
    Settings.init()
