# external imports
from src.Settings import Settings
from src.logger import Logger
from src.DiscordBot import DiscordBot
import asyncio
import time
import importlib
import sys
import os


PRELOADED_MODULES = set(sys.modules.values())


# Imports for code in this project
Settings.init()
logger = Logger(__name__)


def startup_message():
    startup_message = "Discord Bot Startup Began"
    buffer_size = 30
    startup_message = "~"*buffer_size + startup_message + "~"*buffer_size
    logger.info('~'*len(startup_message))
    logger.info(startup_message)
    logger.info('~'*len(startup_message))
    Settings.log()


def reload_modules():
    my_modules = [module for module in (set(sys.modules.values(
    ))-PRELOADED_MODULES) if module.__name__.startswith("src")]
    log_msg = "Reloading Modules\n"
    buffer = " "*50

    for module in my_modules:
        try:
            importlib.reload(module)
            log_msg += buffer + 'reloaded: ' + str(module) + "\n"

        except:
            log_msg += buffer + "Did not reload: " + str(module) + "\n"
    Settings.init()
    logger = Logger(__name__)
    logger.debug(log_msg)


async def main():

    run_status = True
    startup_message()
    generate_directories()
    while run_status:
        logger.info("Launching Bot")
        bot = await DiscordBot.initialize_bot(SQLITE_DB_PATH=Settings.get('SQLITE_DB_PATH'), SQLITE_DB_FILE=Settings.get('SQLITE_DB_FILE'))
        await bot.runBot()
        run_status = await bot.getRunStatus()
        await bot.disconnect_timeout(timeout=float(Settings.get("timeout_duration")), interval=float(Settings.get('timeout_interval')))
        time.sleep(2)
        if run_status:
            logger.info("Bot is restarting")
            reload_modules()
        else:
            logger.info("Bot is shutting down.")




def generate_directories() -> bool:
    directories = [ "logs/nicknames", "settings", "data/audio/clips","data/audio/users", "data/images"]
    successful = True
    for dir in directories:
        if not(os.path.isdir(dir)):
            os.makedirs(dir)
        successful = successful if os.path.isdir(dir) else False
    return successful

if __name__ == "__main__":
    asyncio.run(main())

