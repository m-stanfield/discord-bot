#external imports
import asyncio
import time
import importlib 
import sys

PRELOADED_MODULES = set(sys.modules.values())


# Imports for code in this project
from src.DiscordBot import DiscordBot
from src.logging.logger import Logger
from src.common.Settings import Settings

logger = Logger(__name__)
settings = Settings.init()




def startup_message():
    startup_message = "Discord Bot Startup Began"
    buffer_size = 30
    startup_message = "~"*buffer_size + startup_message + "~"*buffer_size
    logger.info('~'*len(startup_message))
    logger.info(startup_message)
    logger.info('~'*len(startup_message))
    Settings.log()

def reload_modules():
    my_modules = [module for module in (set(sys.modules.values())-PRELOADED_MODULES) if module.__name__.startswith("src")]
    log_msg = "Reloading Modules\n"
    buffer = " "*50
    
    for module in my_modules:
        try:
            importlib.reload(module)
            log_msg += buffer + 'reloaded: '+ str(module) + "\n"

        except :
            log_msg += buffer + "Did not reload: " + str(module) + "\n"
    logger = Logger(__name__)
    logger.debug(log_msg)
    Settings.init()

async def main():
    run_status = True
    startup_message()
    while run_status:
        logger.info("Launching Bot")
        bot = DiscordBot(SQLITE_DB=Settings.get('SQLITE_DB'))
        await bot.run()
        run_status = await bot.getRunStatus()
        await bot.disconnect_timeout(timeout=float(Settings.get("timeout_duration")), interval=float(Settings.get('timeout_interval')))
        time.sleep(2)
        if run_status:
            logger.info("Bot is restarting")
            reload_modules()
        else:
            logger.info("Bot is shutting down.")




if __name__ == "__main__":

    asyncio.run(main())







