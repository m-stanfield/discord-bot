from dataclasses import asdict, dataclass
import dataclasses
from dataclasses import InitVar
from copy import deepcopy
import time
from typing import Any
@dataclass
class BaseSchema:
    TABLE_NAME = None
    reset: InitVar[bool] = None
    table_dict: InitVar[dict|None] = None
    def __post_init__(self, reset:bool=True,table_dict:dict|None=None):
        if reset:
            self.reset()
        if table_dict is not None and isinstance(table_dict, dict):
            for key in table_dict.keys():
                if key in self.__dict__:
                    self.__dict__[key] = table_dict[key]


    def copy(self):
        return deepcopy(self)

    def drop(self, keys:list[str]):
        for key in keys:
            if key in self.__dict__.keys():
                self.__dict__[key] = None

    def pop(self, key:str, default:Any=None):
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
        for key,val in dictionary.items():
            if val is not None:
                output[key] = val
        return output

    @classmethod
    def getTableName(self):
        name = self.__name__.replace("Schema","").lower()
        return name
    
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
    guild_name:str = 'default_guild_name'
    guild_id:int = '-1'
    audio_enabled:int = '0'


@dataclass
class UserSchema(BaseSchema):
    guild_name:str = 'default_name'
    guild_id:int = -1
    user_id:int = -1
    user_name:str = "default_name"
    nickname:str = "nickname"
    default_nickname:str = "default_name"
    volume:float = 0.5
    length:float = 3.0
    superuser:int = 0
    ban:int = 0
    ban_count:int = 0
    custom_audio:float = 1.0
    enable_logging:int = 0
    unique_settings:int = 0
    audio_enabled:int = 1
    solo_play:int = 0

@dataclass
class NicknamesSchema(BaseSchema):
    guild_name:str = 'default_name'
    guild_id:int = -1
    user_id:int = -1
    user_name:str = "default_name"
    nickname:str = "nickname"
    timestamp:float = -1.0

    def setTime(self, timestamp:float|None=None):
        self.timestamp = timestamp if timestamp is not None else time.time()




def _generateSchemaDict(var_dict:dict):
    keys = var_dict.keys()
    value_dict = {}
    for key in keys:

        if dataclasses.is_dataclass(var_dict[key]) and key != BaseSchema.__name__:

            value_dict[var_dict[key]().getTableName()] = {field.name:PyToSQLConverter(field.default) for field in dataclasses.fields(var_dict[key])}
    
    return value_dict

schema_dict =  _generateSchemaDict(var_dict=vars())


if __name__  == "__main__":
    print(schema_dict)
    
    
    for tableName,tableSchema in schema_dict.items():
        print(f"\nTable {tableName}")
        for key, entry in tableSchema.items():
            print(f"{key} ({entry[1]}): {entry[0]}")

    user = UserSchema(table_dict={"solo_play":1})
    for val in user:
        print('val: ',val)
    print(user.getTableName())
    print(user)
    print(user.toDict())

    guild = GuildSchema(reset=False)
    print(guild.getTableName())
    print(guild)
    print(guild.toDict())
    