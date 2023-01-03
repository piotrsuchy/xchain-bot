import csv
import requests as rq
import pandas as pd

# Set the API endpoint URL
endpoint = 'https://xchain.io/api/dispenses/'

def get_dispenses(assets):
    # Set the initial page number and page size
    page = 100
    page_size = 100

    # Initialize an empty list to store the data
    data = []

    # Set a flag to indicate when there are no more pages of data
    more_pages = True

    # Loop until there are no more pages of data
    while more_pages:
        # Construct the full API URL with the current page and page size
        url = f'{endpoint}?page={page}&page_size={page_size}'

        # Make the request to the API
        response = rq.get(url)

        # Parse the JSON data
        new_data = response.json()['data']

        # Add the new data to the existing data
        data.extend(new_data)

        # Check if there are more pages of data
        if page > 120:
            more_pages = False
        else:
            # Increment the page number for the next iteration
            page += 1

    # Loop through the assets in the list
    for asset in assets:
        # Create a new list containing only rows with the current asset
        filtered_data = [row for row in data if row['asset'] == asset]

        # Save the data to a CSV file if there are any rows that match the current asset
        if filtered_data:
            with open(f'csv_files/dispenses.csv', 'a', newline='') as csvfile:
                fieldnames = ['address', 'asset', 'asset_longname', 'block_index', 'dispenser', 'quantity', 'timestamp', 'tx_hash', 'btc_amount']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

                # Write the field names only if the file is empty
                if csvfile.tell() == 0:
                    writer.writeheader()

                for row in filtered_data:
                    writer.writerow(row)


# df = pd.read_csv('issuances_df.csv')

# asset_array = df['asset'].to_numpy()
# asset
asset_array = ['DAILYSMOL', 'SMOLBTCFAUNA']

get_dispenses(asset_array)