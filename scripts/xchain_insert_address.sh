#!/bin/bash
# bash script that runs the python program and later displays the
# csv file of the scraped address with a column command

# Get the directory of the current script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

# Navigate to the script's directory
cd "$SCRIPT_DIR"
cd ..

# Create the csv_files directory if it doesn't exist
mkdir -p csv_files

# Prompt user for the address and initialization flag
read -p "Enter address to scrape: " address
echo "$address" > input_from_script.txt

read -p "Press '1' if already scraped this address or '0' for first time scraping: " initialized_flag
echo "$initialized_flag" >> input_from_script.txt

# Set the RUNNING_THROUGH_BASH_SCRIPT variable to ensure correct execution flow
export RUNNING_THROUGH_BASH_SCRIPT=1

# Run the Python script with input redirection from file
python3 main.py < input_from_script.txt

# Navigate to the 'csv_files' directory
cd csv_files

# Create the csv file with the specified address if it doesn't exist
csv_file="asset_dispenses_${address}.csv"
touch "$csv_file" # This will create the file if it does not exist

# Display the CSV file content in a tabulated format
column -s, -t < "$csv_file" | less -N -S

# Reset the RUNNING_THROUGH_BASH_SCRIPT variable
export RUNNING_THROUGH_BASH_SCRIPT=0
