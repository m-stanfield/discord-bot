#!/bin/bash

screen -dmS discord bash -c 'source activate discord; python cogs/cog_generators/image_cog_gen.py; python bot_base.py'
