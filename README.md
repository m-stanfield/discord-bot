# discord-bot

A bot that will play customizable audio 'intros' whenever a user joins a voice channel on discord, along with a few other fun features. With the intro, users can tell who has joined the voice chat without needing to swap from whatever game or application they are currently in. Usingg the discord.py API.

## Features

* Plays unique audio clip for each user who joins a Discord voice chat
* Default text-to-speech audio file of user's current server nickname
* Can set random chance to play custom intro vs default intro.
* Per users definable settings for settings like clip volume, clip length, solo play, ect.
* Settings and audio clips are defined on a per server basis, allowing a single user to have different intros for different servers.
* Prevents other users from changing others settings, unless a user has been given bot Admin settings.
* Enables 'big emotes', or images which get posted when a user call an image specific '!' command.
* Keeps a log of user nicknames that users can check if they want to see how long they had a previous nickname.

## Install Instructions

An setup script(```initial_install.sh```) has been written to assist the install process. Install process was done on Ubuntu and requires an Anaconda install.

Install script will install required packages using ```sudo apt install``` and ```pip install```.

Creates a new conda enviroment called ```discord```.

## Program Stucture

The program is structured into a base file (```bot_base.py```) and cog files.

The base file loads the individual cogs and initializes the bot and SQL database.

The cogs are seperated out into the various aspects of the program they control, such as guild or users settings.

The current cogs are:

* ```base```: Contains the functions that update on state changes from the API. Primaily the different listener functions for events such as a new user joining server or a voice channel.
* ```general```: Contains associate/general user facing functions.
* ```guild```: Contains functions that are related to individual guild settings.
* ```user```: Contains internal functions and user calls related to an individual user.
* ```image```: Auto-generated cog that adds functions based off of all image files in the images folder. Automatically assigns all image names to '!' commands with the same name as the image file. Code used to generate the cog is in ```cogs/cog_generators/image_cog_gen.py``` with adds to the code in ```cogs/cog_base/image_cog_base.py```. 

