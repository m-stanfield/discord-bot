#!/bin/bash


sudo apt update
sudo pat install postgresql postgresql-contrib

sudo -u postgres createuser discordbot
sudo -u postgres createdb server_settings
sudo -u postgres psql -c "ALTER USER discordbot PASSWORD 'discordbotpassword';"
sudo -u postgres psql -c "grant all privileges on database server_settings to discordbot;"
