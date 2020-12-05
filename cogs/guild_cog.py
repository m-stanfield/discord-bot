from discord.ext import commands
import os
import sys
sys.path.append('functions')
import profile_fun as pf


class guilds(commands.Cog):
    def __init__(self, bot):
        print('Cog Loaded: guilds')
        self.bot = bot

    def load_defaults(self, directory=None):
        if directory == None:
            path = 'guild_defaults.dat'
        else:
            path = directory + '/guild_defaults.dat'

        if os.path.exists(path):
            with open(path,'r') as f:
                content = f.readlines()
            
            
            content = [x.strip().replace('\t','').replace(' ','')  for x in content] 
            dic = {}
            for line in content:
                if len(line) > 0:
                    a = line.split('=')
                    varname = a[0]
                    vartype = a[1].split(':')[0]
                    varval = a[1].split(':')[1]
                    


                    if vartype == 'BOOL':
                        dic[a[0]] = ('BOOL',bool(int(varval)))
                    elif vartype == 'TEXT':
                        dic[a[0]] = ('TEXT',varval.replace('"',"'"))
                    elif vartype == 'FLOAT':
                        dic[a[0]] = ('FLOAT',float(varval))
                    elif vartype == 'BIGINT':
                        dic[a[0]] = ('BIGINT',int(varval))
                    else:
                        try:
                            dic[a[0]] = ('BIGINT',int(varval))
                        except ValueError:
                            dic[a[0]] = ('TEXT',str(varval))
                    
            return dic
        else:
            return {}    
        
        