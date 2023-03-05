import requests as rq
import pandas as pd
from datetime import datetime
from src.scraping_functions import get_address_assets_info, get_dispenses_from_assets, clean_dispenses_csv, scrape_dispenses

'''
Initial script that goes through every asset from csv/files/issuances_df.csv and checks their
dispenses and writes it down to a csv file converting the timestamp to human format
if initialized flag is on the script will instead go through the dispenses section directly and 
check for assets from the address given until the last timestamp is reached 
'''


def main():
    address_to_scrape = input("Paste an address to scrape: ")

    # timestamps in both formats:
    current_time = datetime.now()
    formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
    unix_timestamp = datetime.now().timestamp()

    # flag to get first data from assets if the .csv files are not there:
    initialized = input(
        "Already scraped this address - press '1' or first time scraping this address - press 0:"
    )
    if not int(initialized):
        # creating a issuances_{address}.csv
        get_address_assets_info(address_to_scrape)
        # dataframe from a csv_file that is later used to get an array of assets created by that address
        df_of_issuances = pd.read_csv(
            f'csv_files/issuances_{address_to_scrape}.csv')
        asset_array = df_of_issuances['asset'].to_numpy()
        # getting dispenses from assets one by one
        get_dispenses_from_assets(address_to_scrape, asset_array,
                                  formatted_time)
        clean_dispenses_csv(address_to_scrape, formatted_time)
    else:
        # dataframe from a csv_file that is later used to get an array of assets created by that address
        df_of_issuances = pd.read_csv(
            f'csv_files/issuances_{address_to_scrape}.csv')
        asset_array = df_of_issuances['asset'].to_numpy()
        scrape_dispenses(address_to_scrape, asset_array, unix_timestamp)

    # the code above takes a lot of time, so if i run this program every day or so,
    # it's better to get next data straight from url endpoint of api/dispenses/ until
    # we run into a block or timestamp of the last time this program was run:


if __name__ == "__main__":
    main()
