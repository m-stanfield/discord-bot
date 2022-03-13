from dataclasses import dataclass
import dataclasses
from dataclasses import InitVar

@dataclass
class BaseSchema:
    reset: InitVar[bool] = None
    member_dict: InitVar[dict|None] = None
    def __post_init__(self, reset:bool=True,member_dict:dict|None=None):
        if reset:
            self.reset()
        if member_dict is not None and isinstance(member_dict, dict):
            for key in member_dict.keys():
                if key in self.__dict__:
                    self.__dict__[key] = member_dict[key]

    def reset(self):

        for key in self.__dict__:
            self.__dict__[key] = None
    
    def __str__(self):
        output = ""
        for key in self.__dict__:
            output += f"{key}: {self.__dict__[key]}\n"
        return output

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

    return value, sql_type

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





def _generateSchemaDict(var_dict:dict):
    keys = var_dict.keys()
    value_dict = {}
    for key in keys:

        if dataclasses.is_dataclass(var_dict[key]) and key != BaseSchema.__name__:

            value_dict[key.replace("Schema","").lower()] = {field.name:PyToSQLConverter(field.default) for field in dataclasses.fields(var_dict[key])}
    
    return value_dict

schema_dict =  _generateSchemaDict(var_dict=vars())

if __name__  == "__main__":
    print(schema_dict.keys())

    
    for tableName,tableSchema in schema_dict.items():
        print(f"\nTable {tableName}")
        for key, entry in tableSchema.items():
            print(f"{key} ({entry[1]}): {entry[0]}")

    user = UserSchema(member_dict={"solo_play":1})
    print('user')
    print(user)
    