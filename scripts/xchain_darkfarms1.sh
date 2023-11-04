#!/bin/bash
# The script for checking Darkfarms1's (my favourite cryptoartist) xchain address

# change the flag "second_input" to 1 after first run of the script

# setting a variable to print input prompts only when running not through console
export RUNNING_THROUGH_BASH_SCRIPT=1

# Get the directory of the current script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

# Change to the script's directory
cd "$SCRIPT_DIR"

# Go up one directory from script location
cd ..

# Create a directory named 'csv_files' if it doesn't exist
mkdir -p csv_files

# Set the fixed values for the input
address="1DRZVQe58Tr9WxDNYdJUbye3toH1zkedX"
initialized_flag="1"

# Write values to input_from_script.txt
echo "$address" > input_from_script.txt
echo "$initialized_flag" >> input_from_script.txt

# Inform user of the process
echo "Scraping address $address"
echo "With the initialized flag equal to $initialized_flag." 
echo "Please wait:" 
echo

# Run the python script with input redirection
python3 main.py < input_from_script.txt

# Navigate to the 'csv_files' directory
cd csv_files

# Create the csv file if it doesn't exist
touch "asset_dispenses_${address}.csv"

# Output the contents of the csv file in a formatted table view
column -s, -t < "asset_dispenses_${address}.csv" | less -N -S

# Reset the variable after running the script
export RUNNING_THROUGH_BASH_SCRIPT=0
