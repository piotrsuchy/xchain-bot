#!/bin/bash
# The script for checking Darkfarms1's (my favourite cryptoartist) xchain address

# change the flag "second_input" to 1 after first run of the script

# setting a variable to print input prompts only when running not through console
export RUNNING_THROUGH_BASH_SCRIPT=1

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

cd $SCRIPT_DIR
cd ..

# Set the fixed values for the input
address="1DRZVQe58Tr9WxDNYdJUbye3toH1zkedX"
initialized_flag="1"

echo "$address" > input_from_script.txt
echo "$initialized_flag" >> input_from_script.txt

echo Scraping address $address
echo With the the initialized flag equal to $initialized_flag. 
echo Please wait: 
echo

python3 main.py < input_from_script.txt

cd csv_files
column -s, -t < asset_dispenses_1DRZVQe58Tr9WxDNYdJUbye3toH1zkedX.csv | less -N -S

export RUNNING_THROUGH_BASH_SCRIPT=0

