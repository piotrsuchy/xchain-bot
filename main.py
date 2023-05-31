import requests as rq
import pandas as pd
from datetime import datetime
from src.scraping_functions import get_address_assets_info, get_dispenses_from_assets, clean_dispenses_csv, scrape_dispenses
import os
'''
Initial script that goes through every asset from csv/files/issuances_df.csv and checks their
dispenses and writes it down to a csv file converting the timestamp to human format
if initialized flag is on the script will instead go through the dispenses section directly and 
check for assets from the address given until the last timestamp is reached 
'''


def get_asset_array(address):
    df_of_issuances = pd.read_csv(f'csv_files/issuances_{address}.csv')
    asset_array = df_of_issuances['asset'].to_numpy()
    return asset_array


def main():
    try:
        if os.environ.get('RUNNING_THROUGH_BASH_SCRIPT'):
            PRINT_ENABLED = False
        else:
            PRINT_ENABLED = True

        if PRINT_ENABLED:
            address_to_scrape = input("Paste an address to scrape: ")
            # flag to get first data from assets if the .csv files are not there:
            initialized = input(
                "Already scraped this address - press '1' or first time scraping this address - press 0: "
            )
        else:
            address_to_scrape = input()
            initialized = input()

        # timestamps in both formats:
        current_time = datetime.now()
        formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
        unix_timestamp = datetime.now().timestamp()

        if not int(initialized):
            # creating a issuances_{address}.csv
            get_address_assets_info(address_to_scrape)
            # dataframe from a csv_file that is later used to get an array of assets created by that address
            asset_array = get_asset_array(address_to_scrape)
            # getting dispenses from assets one by one
            get_dispenses_from_assets(address_to_scrape, asset_array,
                                      formatted_time)
            clean_dispenses_csv(address_to_scrape, formatted_time)
        else:
            # dataframe from a csv_file that is later used to get an array of assets created by that address
            asset_array = get_asset_array(address_to_scrape)
            scrape_dispenses(address_to_scrape, asset_array, unix_timestamp)
    except Exception as e:
        print(f"An error occurred: {e}")
    # the code above takes a lot of time, so if i run this program every day or so,
    # it's better to get next data straight from url endpoint of api/dispenses/ until
    # we run into a block or timestamp of the last time this program was run:


if __name__ == "__main__":
    main()
