import csv
import requests as rq
import pandas as pd


# Set the API endpoint URL
endpoint = 'https://xchain.io/api/dispenses/'

def get_dispenses_from_assets(assets):
    # Set the field names for the CSV file
    fields = ['address', 'asset', 'asset_longname', 'block_index', 'btc_amount', 'dispenser', 'quantity', 'timestamp', 'tx_hash']

    # Open the file in write mode
    with open('csv_files/asset_disp.csv', 'w', newline='') as csvfile:
        # Create a csv.writer instance
        writer = csv.writer(csvfile)
        
        # Write the header row
        writer.writerow(fields)
        
        # Iterate over the assets in assets
        for asset in assets:
            url = '{0}/{1}'.format(endpoint, asset)
    
            # Make the request to the API
            response = rq.get(url)
            
            new_data = response.json()['data']

            # Iterate over the items in new_data
            for item in new_data:
                # Write each item to the file as a separate row
                writer.writerow([item[field] for field in fields])


df = pd.read_csv('csv_files/issuances_df.csv')

asset_array = df['asset'].to_numpy()
# asset

# asset_array = ['SMOLBTCFAUNA', 'DAILYSMOL']

get_dispenses_from_assets(asset_array)