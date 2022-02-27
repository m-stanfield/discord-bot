import sqlite3
import logging
import os
print(os.getcwd())
from src.logging.logger import Logger

logger = Logger(__name__,{'level':logging.INFO})


con = sqlite3.connect("data/database/discord_bot.db")
logger.info("DataBase Init")
logger.debug("DataBase Init: debug")
