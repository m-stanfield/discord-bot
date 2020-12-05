#!/bin/bash

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
