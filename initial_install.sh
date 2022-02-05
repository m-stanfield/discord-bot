#!/bin/bash

mkdir audio
mkdir audio/clips
mkdir audio/users

mkdir images

mkdir logs
mkdir logs/nicknames

mkdir settings
sudo apt update
sudo apt install postgresql postgresql-contrib
sudo apt install ffmpeg
conda create --name=discord python=3.6
source activate discord
pip install -U "discord.py[voice]"
pip install python-dotenv
pip install numpy
conda install h5py
pip install asyncpg
pip install gTTS
pip install PyYAML
pip install git+https://github.com/SamHDev/insiro.git
