#!/bin/bash

mkdir data/audio
mkdir data/audio/clips
mkdir data/audio/users

mkdir data/images

mkdir data/logs
mkdir data/logs/nicknames

mkdir data/settings
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
