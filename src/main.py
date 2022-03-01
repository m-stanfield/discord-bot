from DiscordBot import DiscordBot
import asyncio
import logging
from src.logging.logger import Logger
import argparse
import os
from misc.Settings import Settings
# globals
logger = Logger(__name__)

async def main():
    SETTINGS = Settings()
    startup_message = "Discord Bot Startup Began"
    buffer_size = 30
    startup_message = "~"*buffer_size + startup_message + "~"*buffer_size
    logger.info('~'*len(startup_message))
    logger.info(startup_message)
    logger.info('~'*len(startup_message))
    SETTINGS.log()

    bot = DiscordBot(SQLITE_DB=SETTINGS.get('SQLITE_DB'))

    run_state = True
    if SETTINGS.get('TEST_LOAD') == 1:
        logger.info("Load was successful. Due to test load being enabled program will now exit.")
        run_state = False

    while run_state:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(await bot.run())
    logger.info("Program Closed")


if __name__ == "__main__":
    asyncio.run(main())





