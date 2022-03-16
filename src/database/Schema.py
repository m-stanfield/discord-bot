from abc import abstractmethod, ABC
from dataclasses import asdict, dataclass
import dataclasses
from dataclasses import InitVar
from copy import deepcopy
import time
from typing import Any


@dataclass
class BaseSchema(ABC):
    table_dict: InitVar[dict | None] = None

    def __init__(self, **kwargs):
        self.reset()

        for key, value in kwargs.items():
            if key in self.__dict__.keys():
                setattr(self, key, value)


    @abstractmethod
    def toSearch(self):
        pass

    def copy(self):
        return deepcopy(self)

    def drop(self, keys: list[str]):
        for key in keys:
            if key in self.__dict__.keys():
                self.__dict__[key] = None

    def pop(self, key: str, default: Any = None):
        popped_val = default
        if key in self.__dict__.keys():
            popped_val = self.__dict__[key]
            self.drop(key)
        return popped_val

    def reset(self):
        for key in self.__dict__:
            self.__dict__[key] = None

    def toDict(self):
        dictionary = asdict(self)
        output = {}
        for key, val in dictionary.items():
            if val is not None:
                output[key] = val
        return output

    @classmethod
    def getTableName(self):
        name = self.__name__.replace("Schema", "").lower()
        return name

    def allKeys(self):
        return self.__dict__.keys()

    def allItems(self):
        return self.__dict__.items() 

    def keys(self):
        temp_dict = {key:value for key, value in self.__dict__.items() if value is not None}
        return temp_dict.keys()

    def items(self):
        temp_dict = {key:value for key, value in self.__dict__.items() if value is not None}
        return temp_dict.items()

    def __str__(self):
        output = ""
        for key in self.__dict__:
            output += f"{key}: {self.__dict__[key]}\n"
        return output

    def __iter__(self):
        yield from self.__dict__.items()


def PyToSQLConverter(value):
    val_type = type(value)
    sql_type = "BLOB"
    if val_type is float:
        sql_type = "REAL"
        value = float(value)
    elif val_type is int or val_type is bool:
        sql_type = "INTEGER"
        value = int(value)
    elif val_type is str:
        sql_type = "TEXT"
        value = str(value)

    return sql_type, value


@dataclass
class GuildSchema(BaseSchema):
    guild_name: str = 'default_guild_name'
    guild_id: int = '-1'
    audio_enabled: int = '0'

    def toSearch(self):
        search_dict = {}
        search_dict['guild_id'] = self.guild_id
        return search_dict


@dataclass
class UserSchema(BaseSchema):
    guild_name: str = 'default_name'
    guild_id: int = -1
    user_id: int = -1
    user_name: str = "default_name"
    nickname: str = "nickname"
    default_nickname: str = "default_name"
    volume: float = 0.5
    length: float = 3.0
    superuser: int = 0
    ban: int = 0
    ban_count: int = 0
    custom_audio: float = 1.0
    enable_logging: int = 0
    unique_settings: int = 0
    audio_enabled: int = 1
    solo_play: int = 0
    audio_path: str = None

    def toSearch(self):
        search_dict = {}
        search_dict['guild_id'] = self.guild_id
        search_dict['user_id'] = self.user_id
        return search_dict


@dataclass
class NicknamesSchema(BaseSchema):
    guild_name: str = 'default_name'
    guild_id: int = -1
    user_id: int = -1
    user_name: str = "default_name"
    nickname: str = "nickname"
    timestamp: float = -1.0

    def setTime(self, timestamp: float = -1):
        self.timestamp = timestamp if timestamp > 0 else time.time()

    def toSearch(self):
        search_dict = {}
        search_dict['guild_id'] = self.guild_id
        search_dict['user_id'] = self.user_id
        search_dict['timestamp'] = self.timestamp
        return search_dict


def _generateSchemaDict(var_dict: dict) -> dict:
    keys = var_dict.keys()
    value_dict = {}
    for key in keys:

        if dataclasses.is_dataclass(var_dict[key]) and key != BaseSchema.__name__:

            value_dict[var_dict[key]().getTableName()] = {field.name: PyToSQLConverter(
                field.default) for field in dataclasses.fields(var_dict[key])}

    return value_dict


SCHEMA_DICT = _generateSchemaDict(var_dict=vars())


if __name__ == "__main__":
    print(SCHEMA_DICT)

    for tableName, tableSchema in SCHEMA_DICT.items():
        print(f"\nTable {tableName}")
        for key, entry in tableSchema.items():
            print(f"{key} ({entry[1]}): {entry[0]}")

    user = UserSchema(table_dict={"solo_play": 1})
    for val in user:
        print('val: ', val)
    print(user.getTableName())
    print(user)
    print(user.toDict())

    guild = GuildSchema()
    print(guild.getTableName())
    print(guild)
    print(guild.toDict())

    nick = NicknamesSchema()
    print(nick.timestamp)
    nick2 = NicknamesSchema()
