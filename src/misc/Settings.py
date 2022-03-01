import argparse
import dotenv
import os

from src.logging.logger import Logger

logger = Logger(__name__)


class Settings:
    settings: dict | None = None

    def __init__(self):
        if self.settings is None:
            self.settings = {}
            self._load_env()
            self._parseArgs()

    def __str__(self):
        output = ""
        for i, key in enumerate(self.settings):
            if i > 0:
                output += "\n"
            output += self._key2Str(key)
        return output

    def get(self, key: str):
        return self.settings[key]

    def getSettings(self):
        return dict(self.settings)

    def getKeys(self):
        return self.settings.keys()

    def keys(self):
        return self.getKeys()

    def _key2Str(self, key:str)->str:
        output:str
        if key.endswith("TOKEN"):
            output = f"{key}: REDACTED"
        else:
            output = f"{key}: {self.settings[key]}"
        return output

    def log(self):
        logger.info("Logging discord bot initilization settings")
        key:str
        for key in self.settings:
            logger.info(self._key2Str(key))


    def _load_env(self):
        dotenv.load_dotenv()

        env = ["DISCORD_TOKEN", "SQLITE_DB"]

        for key in env:
            try:
                self.settings[key] = os.getenv(key)
            except KeyError:
                logger.error(f"Invalid enrivoment key on load: {key}")

    def _parseArgs(self):
        parser = argparse.ArgumentParser(
            description="Sets runtime settings for discord bot")
        parser.add_argument('--TEST_MODE', type=int, default=0)
        parser.add_argument('--UPDATE_ALL', type=int, default=1)
        parser.add_argument('--DISABLE_WAKEUP', type=int, default=0)
        parser.add_argument('--TEST_LOAD', type=int, default=0)
        parser.add_argument('--LOG', type=int, default=None)
        args = parser.parse_args()

        for key in vars(args):
            self.settings[key] = vars(args)[key]

if __name__ == "__main__":
    SETTINGS = Settings()
    print(SETTINGS)

