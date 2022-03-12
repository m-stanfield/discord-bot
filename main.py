#external imports
import asyncio
import time
import importlib 
import sys

PRELOADED_MODULES = set(sys.modules.values())


# Imports for code in this project
import src.DiscordBot as DiscordBot
import src.logging.logger as Logger
import src.common.Settings as Settings

logger = None

def startup_message():
    startup_message = "Discord Bot Startup Began"
    buffer_size = 30
    startup_message = "~"*buffer_size + startup_message + "~"*buffer_size
    logger.info('~'*len(startup_message))
    logger.info(startup_message)
    logger.info('~'*len(startup_message))
    Settings.Settings.log()

def reload_modules():
    my_modules = [module for module in (set(sys.modules.values())-PRELOADED_MODULES) if module.__name__.startswith("src")]
    for module in my_modules:
        try:
            importlib.reload(module)
            print('reloaded: ', module)

        except :
            print("Did not reload: ",module)
    logger = Logger.Logger(__name__)
    Settings.Settings.init()

async def main():
    run_status = True
    startup_message()
    while run_status:
        logger.info("Launching Bot")
        bot = DiscordBot.DiscordBot(SQLITE_DB=Settings.Settings.get('SQLITE_DB'))
        await bot.run()
        run_status = bot.getRunStatus()
        time.sleep(3)
        if run_status:
            logger.info("Bot is restarting")
            reload_modules()
        else:
            logger.info("Bot is shutting down.")




if __name__ == "__main__":
    logger = Logger.Logger(__name__)
    Settings.Settings.init()
    asyncio.run(main())







