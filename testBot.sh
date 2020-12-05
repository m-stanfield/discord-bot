#!/bin/bash

source activate discord

# TODO: Create audio and image script genearting code

python cogs/cog_generators/image_cog_gen.py
python bot_base.py --TEST_MODE 1
