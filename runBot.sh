#!/bin/bash

screen -dmS discord bash -c 'source activate discord; python src/cogs/cog_generators/image_cog_gen.py; python src/bot_base.py --LOG 1'
