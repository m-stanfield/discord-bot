
import numpy as np
import glob
import argparse

import os

'''
Short script to generate user callable functions to post images onto chat.
Base code pulled from image_cog_base.py and each image has file create from the
file name. Callable using !<image_name> command in discord.
'''
def generate_images():
    print('Generating image_cog.py')

    parser = argparse.ArgumentParser(description="Sets runtime settings for discord bot")
    parser.add_argument('--basepath', type=str,default='cogs/cog_base')
    parser.add_argument('--imagepath', type=str,default='images/')
    parser.add_argument('--cogpath', type=str,default='cogs/')

    args = parser.parse_args()

    pathList = glob.glob(args.imagepath + '*.png')
    pathList = glob.glob(args.imagepath + '*.gif') + pathList
    pathList = glob.glob(args.imagepath + '*.jpg') + pathList
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


    with open(args.basepath + '/image_cog_base.py','r') as f:
        string = f.read()
    string += '\n\n'

    for idx in range(len(fileList)):
        string += "\t@commands.command()\n\tasync def %s(self,ctx):\n\t\tawait self.post_image(ctx,'%s')\n\n\n"%(fileList[idx],pathList[idx])
    string = string.replace('\t','    ')
    with open('cogs/image_cog.py','w') as f:
        print(string,file=f)
    print(displayStr)


if __name__ == '__main__':
    generate_images()  
