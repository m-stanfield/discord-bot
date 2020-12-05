import h5py
import numpy as np
import glob
import re
import discord

def mention_to_id(mention):
    return int(re.sub("[^0-9]", "", mention))
    

def mention_to_user(guild,mention):
    return discord.utils.get(guild.members, id=mention_to_id(mention))

def find_member(guild,ctx,mention):
   # print(mention)
    if mention != None:
        member = mention_to_user(guild,mention)
    else:
        member = ctx.author
    return member



    
def roll_dice(args):
    """Inputs: Dice roll represented in terms of XdY+AxB-Z"""  
    #await ctx.message.delete()
    diceString = ''
    for ele in args:
        diceString += ele

    def diceRoller(diceString):
        a = diceString.split('d')
        numDice = int(a[0])
        diceSize = int(a[1])

        roll = np.random.randint(1,diceSize+1,numDice)
        return roll
    diceString = diceString.replace(' ','')
    splitstr = diceString.split('+')
    for ii in range(len(splitstr)):
        splitstr[ii] = splitstr[ii].split('-')
    output = ''
    result = 0
    
    for ii, dicelist in enumerate(splitstr):
        for jj, dicestring in enumerate(dicelist):
            if dicestring.find('d') != -1:
                roll = diceRoller(dicestring)
            else:
                roll = np.array([int(dicestring)])
            if jj == 0:
                result += np.sum(roll)
                if ii == 0:
                    for kk,num in enumerate(roll):
                        if kk == 0:
                            output+='(%d'%num
                        else:
                            output += ' + %d'%num
                    output += ')'

                else:
                    for kk,num in enumerate(roll):
                        if kk == 0:
                            output+=' + (%d'%num
                        else:
                            output += ' + %d'%num
                    output += ')'

            else:
                result -= np.sum(roll)
                if ii == 0:
                    for kk,num in enumerate(roll):
                        if kk == 0:
                            output+='(%d'%num
                        else:
                            output += ' + %d'%num
                    output += ')'

                else:
                    for kk,num in enumerate(roll):
                        if kk == 0:
                            output+=' - (%d'%num
                        else:
                            output += ' + %d'%num
                    output += ')'
#print(str(result) + ' = ' + output)
    
    return 'Total: %d    Breakdown: %s'%(result,output)




