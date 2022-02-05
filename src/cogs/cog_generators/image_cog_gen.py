
import numpy as np
import glob

import os

import logging

logger = logging.getLogger(__name__)

'''
Short script to generate user callable functions to post images onto chat.
Base code pulled from image_cog_base.py and each image has file create from the
file name. Callable using !<image_name> command in discord.
'''
def generate_images():
    logger.info('Generating image_cog.py')

    imagepath = "data/images/"
    cogpath = "src/cogs/"
    basepath = "src/cogs/cog_base"
    pathList = glob.glob(imagepath + '*.png')
    pathList = glob.glob(imagepath + '*.gif') + pathList
    pathList = glob.glob(imagepath + '*.jpg') + pathList
    fileList = []
    longestLen = 0
    lengths = []
    for idx in range(len(pathList)):
        fileList.append(pathList[idx].replace('\\','/').split('/')[-1][0:-4].lower())
        lengths.append(len(fileList[idx]))
        if len(fileList[idx]) > longestLen:
            longestLen = len(fileList[idx])

    message = '       Images added to image_cog       '
    displayStr = ''
    displayStr +='\n' + '-'*len(message)
    displayStr +='\n' + message
    displayStr +='\n' + '-'*len(message) + '\n'


    for ii in range(len(fileList)):
        displayStr += fileList[ii]
        if (ii+1)%5==0:
            displayStr += '\n'
        else:
            displayStr += ' '*(int((longestLen-lengths[ii]))+3)

    displayStr +='\n' + '-'*len(message) + '\n'

    string = ''


    with open(basepath + '/image_cog_base.py','r') as f:
        string = f.read()
    string += '\n\n'

    for idx in range(len(fileList)):
        string += "\t@commands.command()\n\tasync def %s(self,ctx):\n\t\tawait self.post_image(ctx,'%s')\n\n\n"%(fileList[idx],pathList[idx])
    string = string.replace('\t','    ')
    with open(cogpath + '/image_cog.py','w') as f:
        print(string,file=f)
    print(displayStr)


if __name__ == '__main__':
    generate_images()  
