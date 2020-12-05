#!/bin/bash

sudo -u postgres createuser discordbot
sudo -u postgres createdb server_settings
#sudo -u postgres psql 'alter user discordbot with encrypted password <password>;'
#sudo -u postgres psql 'grant all privileges on database server_settings to discordbot;'
