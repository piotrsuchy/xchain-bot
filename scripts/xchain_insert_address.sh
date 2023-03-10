#!/bin/bash
# bash script that runs the python program and later displays the 
# csv file of the scraped address with a column command

# change the cd ~/* command to your path to the project folder 
cd ~/Desktop/Programming/PROGRAMMING_PRACTICE/XCHAIN_BOT

read -p "Enter address to scrape: " address
echo $address > input.txt

read -p "Press '1' if already scraped this address or '0' for first time scraping: " initialized_flag
echo $initialized_flag >> input.txt

export RUNNING_THROUGH_BASH_SCRIPT=1

python main.py < input.txt

cd csv_files
csv_file="asset_dispenses_${address}.csv"
column -s, -t < "$csv_file" | less -N -S

export RUNNING_THROUGH_BASH_SCRIPT=0

