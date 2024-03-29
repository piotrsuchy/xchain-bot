import csv
import requests as rq
import pandas as pd
from datetime import datetime


# get issuances from an address
def get_address_assets_info(address):
    try:
        endpoint_address = 'https://xchain.io/api/issuances/'
        assets_written = set()

        # Open a file for writing and create a CSV writer
        with open(f'csv_files/issuances_{address}.csv', 'w',
                  newline='') as csvfile:
            writer = csv.writer(csvfile)
            # Write the header row
            writer.writerow(
                ['asset', 'asset_longname', 'issuer', 'quantity', 'source'])
            # Set the initial page number and page size
            page = 1
            page_size = 100
            # Set a flag to indicate whether there are more pages of data to retrieve
            more_pages = True
            while more_pages:
                url = f'{endpoint_address}{address}?page={page}&page_size={page_size}'
                # Make the request to the API
                response = rq.get(url)
                data = response.json()
                for element in data['data']:
                    # Check if the current asset has already been written to the CSV file
                    if element['asset'] not in assets_written:
                        writer.writerow([
                            element['asset'], element['asset_longname'],
                            element['issuer'], element['quantity'],
                            element['source']
                        ])
                        # Add the current asset to the set of assets that have been written to the CSV file
                        assets_written.add(element['asset'])
                # Check if there are more pages of data to retrieve
                if data['total'] > (page * page_size):
                    # Increment the page number
                    page += 1
                else:
                    # Set the flag to indicate that there are no more pages of data to retrieve
                    more_pages = False
    except Exception as e:
        print(f"An error occurred in get_address_assets_info(): {e}")


# based on a list of assets get dispenses from that assets
def get_dispenses_from_assets(address, assets, formatted_timestamp):
    try:
        fields = [
            'address', 'asset', 'block_index', 'btc_amount', 'dispenser',
            'quantity', 'timestamp'
        ]

        with open(f'csv_files/asset_dispenses_{address}.csv', 'w',
                  newline='') as csvfile:
            # Create a csv.writer instance
            writer = csv.writer(csvfile)

            # Write the header row
            csvfile.write(f"# Last update: {formatted_timestamp}")
            writer.writerow(fields)

            for asset in assets:
                url = 'https://xchain.io/api/dispenses/{0}'.format(asset)

                # Make the request to the API
                response = rq.get(url)

                new_data = response.json()['data']
                # print(new_data)
                # Iterate over the items in new_data
                for item in new_data:
                    timestamp_formatted = datetime.fromtimestamp(
                        item['timestamp'])

                    writer.writerow(
                        [item[field] for field in fields[0:-1]] +
                        [timestamp_formatted.strftime("%Y-%m-%d %H:%M:%S")])
                    # writer.writerow(timestamp_formatted.strftime("%Y-%m-%d %H:%M:%S"))
    except Exception as e:
        print(f"An error occurred in get_dispenses_from_assets(): {e}")


# filtering the dataframe of dispenses by timestamp of dispense:
def clean_dispenses_csv(address, formatted_timestamp):
    try:
        df = pd.read_csv(f'csv_files/asset_dispenses_{address}.csv',
                         comment='#')
        df.columns = [
            'address', 'asset', 'block_index', 'btc_amount', 'dispenser',
            'quantity', 'timestamp'
        ]
        df = df.sort_values(by=['timestamp'], ascending=False)
        df.to_csv(f'csv_files/asset_dispenses_{address}.csv')
        # # Open the original CSV file and create a new temporary file
        # with open('original.csv', 'r') as csv_file, open('temp.csv', 'w', newline='') as temp_file:
        #     # Write the comment line to the temporary file
        #     temp_file.write('# Last update: {}\n'.format(formatted_timestamp))
        #     # Append the original CSV data to the temporary file
        #     temp_file.write(csv_file.read())
        # # Replace the original CSV file with the temporary file
        # os.replace('temp.csv', 'original.csv')
    except Exception as e:
        print(f"An error occurred in clean_dispenses_csv(): {e}")


# scraping until the moment of the timestamp by global dispenses, not by asset dispenses
def scrape_dispenses(address, asset_array, timestamp):
    try:
        fields = [
            'address', 'asset', 'block_index', 'btc_amount', 'dispenser',
            'quantity', 'timestamp'
        ]

        # options for the url to add pagination
        endpoint = 'https://xchain.io/api/dispenses/'
        page = 0
        page_size = 100
        more_pages = True
        flag = 0
        matrix_of_values = []

        while more_pages:
            url = "{0}?page={1}&page_size={2}".format(endpoint, page,
                                                      page_size)
            response = rq.get(url)
            new_data = response.json()['data']
            for item in new_data:
                if item['asset'] in asset_array:
                    values = [item[field] for field in fields]
                    values[-1] = datetime.fromtimestamp(values[-1])
                    matrix_of_values.append(values)
                if int(item['timestamp']) <= int(timestamp):
                    print("Date reached")
                    flag = 1
                    break
            page += 1
            if flag == 1:
                break
        df = pd.DataFrame(matrix_of_values, columns=fields)
        old_df = pd.read_csv(f'csv_files/asset_dispenses_{address}.csv')
        final_df = pd.concat([df, old_df]).drop_duplicates(subset=df.columns,
                                                           keep=False,
                                                           ignore_index=True)
        column_list = final_df.columns.values
        if column_list[-1] == "Unnamed: 0":
            final_df = final_df.drop(columns="Unnamed: 0")

        final_df.to_csv(f'csv_files/asset_dispenses_{address}.csv',
                        index=False)
    except Exception as e:
        print(f"An error occurred in scrape_dispenses(): {e}")