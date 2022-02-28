import sqlite3
from src.logging.logger import Logger

logger = Logger(__name__)


class DataBase:
    #DEFAULT_KWARGS = {'path':':memory:'}#
    DEFAULT_KWARGS = {'path': 'data/database/discord_bot.db'}
    db = None

    def __init__(self, **kwargs):
        self._kwargs = {**self.DEFAULT_KWARGS, **kwargs}
        if self.db is None:
            self.db = sqlite3.connect(self._kwargs['path'])
            logger.info(f"Data has been loaded from : {self._kwargs['path']}")

    def exit(self):
        logger.info(f"Attempting to close database")
        self.db.close()
        logger.info(f"Database was successfully closed")


    def execute(self, command, args=None):
        logger.debug(f"SQL Command: {command}")

        cur = self.db.cursor()
        if args is None:
            cur.execute(command)
        else:
            logger.debug(f"With args: {args}")
            cur.execute(command, args)

    def creatTable(self, tableName, columns, column_types=None):
        # schema_list is tuple/list of tuples/lists of keyword/datatype pairs
        # so ((user_name, text))
        if column_types is not None and not(len(columns) == len(column_types)):
            errormsg = "Column name and type arrays need to have the same length"
            logger.error(errormsg)
            raise ValueError(errormsg)

        column_args = []

        for i in range(len(columns)):
            column_args.append(columns[i])
            if column_types is not None:
                column_args.append(column_types[i])

        # generate command string for creating a table
        cmdstr = f"CREATE TABLE if not exists {tableName} ("
        for i in range(len(columns)):
            # for first element, skip the column
            if i > 0:
                cmdstr += ", "

            # write ? to position the column name
            cmdstr += f"{columns[i]}"

            # if column datatype is given, add ? for its position
            if column_types is not None:
                cmdstr += f" {column_types[i]}"
        cmdstr += ")"

        self.execute(cmdstr)
        return True

    def insert(self, table: str, columns: list, values: list) -> bool:
        if not(len(columns) == len(values)):
            return False

        cmdstr = f"INSERT INTO {table}("

        for idx, elem in enumerate(columns):
            if not(idx == 0):
                cmdstr += ", "
            cmdstr += elem
        cmdstr += ") VALUES ("

        for idx, elem in enumerate(values):
            if not(idx == 0):
                cmdstr += ", "
            if type(elem) is str:
                cmdstr += f'"{elem}"'
            else:
                cmdstr += str(elem)
        cmdstr += ")"

        self.execute(cmdstr)


        return True


if __name__ == "__main__":
    db = DataBase()
    tableName = 'abcde'
    db.creatTable(tableName, columns=['a', 'b', 'c'], column_types=[
                  'int', 'real', 'text'])
    db.insert(tableName, columns=['a', 'b', 'c'], values=[1, 1.0, 'abcd'])
    db.exit()
