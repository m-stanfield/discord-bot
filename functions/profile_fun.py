import h5py
import numpy as np
import glob
import re
import discord

def mention_to_id(mention):
    '''
    converts @mention to user ID
    '''
    return int(re.sub("[^0-9]", "", mention))


def mention_to_user(guild,mention):
    '''
    converts @mention to user info
    '''
    return discord.utils.get(guild.members, id=mention_to_id(mention))

def find_member(guild,ctx,mention):
    '''
    If mention exists converts to member object.
    Otherwise defaults to author's member objects
    '''
    if mention != None:
        member = mention_to_user(guild,mention)
    else:
        member = ctx.author
    return member




def roll_dice(args):
    """Inputs: Dice roll represented in terms of XdY+AxB-Z"""
    #await ctx.message.delete()
    #loading dic string from args
    diceString = ''
    for ele in args:
        diceString += ele
    def diceRoller(diceString):
        #rolls dice of single type(ie 5d6 rolls 5 six sided dice)

        a = diceString.split('d')
        numDice = int(a[0])
        diceSize = int(a[1])

        roll = np.random.randint(1,diceSize+1,numDice)
        return roll

    #formatting string to enable parsing
    #parsing works by removing spaces, spliting on + signs, the spliting on - signs
    #everything in first layer of splitstr adds together.
    #eerything in second layer of splitstr gets subtracted
    diceString = diceString.replace(' ','')
    splitstr = diceString.split('+')
    for ii in range(len(splitstr)):
        splitstr[ii] = splitstr[ii].split('-')
    output = ''
    result = 0


    #enumerating over all of splitstings and strings contined by it
    for ii, dicelist in enumerate(splitstr):
        for jj, dicestring in enumerate(dicelist):
            # if 'd' exists send string to be rolled.
            #othewise its constant and just add it to the roll
            if dicestring.find('d') != -1:
                roll = diceRoller(dicestring)
            else:
                roll = np.array([int(dicestring)])

            #Adds roll to roll total and builds output string based on results
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
