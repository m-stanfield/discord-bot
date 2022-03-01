import sqlite3
import logging
import os
print(os.getcwd())
from src.logging.logger import Logger

logger = Logger(__name__,{'level':logging.INFO})

if __name__ == "__main__":
    con = sqlite3.connect("data/database/discord_bot.db")
    logger.info("DataBase Init")
    cur = con.cursor()
   # cur.execute('''CREATE TABLE stocks (date text, trans text, symbol text, qty real, price real)''')

    cur.execute("INSERT INTO stocks VALUES ('2006-01-05','BUY','RHAT', 100,35)")

    for row in cur.execute('SELECT * FROM stocks ORDER BY price'):
        row_str = ""
        for col in row:
            row_str = f"{row_str}{col}:{type(col)}, "
        print(row_str)
    con.commit()
    con.close()
