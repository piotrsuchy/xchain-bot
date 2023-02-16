import csv
import requests as rq
import pandas as pd
from datetime import datetime

# Initial script that goes through every asset from csv/files/issuances_df.csv and checks their 
# dispenses and writes it down to a csv file converting the timestamp to human format

def get_address_assets_info(address):
    # Set the API endpoint URL
    endpoint_address = 'https://xchain.io/api/issuances/'
    # Create a set to store the assets that have already been written to the CSV file
    assets_written = set()

    # Open a file for writing and create a CSV writer
    with open('csv_files/issuances_df.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        # Write the header row
        writer.writerow(['asset', 'asset_longname', 'issuer', 'quantity', 'source'])
        # Set the initial page number and page size
        page = 1
        page_size = 100
        # Set a flag to indicate whether there are more pages of data to retrieve
        more_pages = True
        # Iterate over the pages of data
        while more_pages:
            # Construct the URL for the current page
            url = f'{endpoint_address}{address}?page={page}&page_size={page_size}'
            # Make the request to the API
            response = rq.get(url)
            # Parse the JSON data
            data = response.json()
            # Iterate over the elements in the data list
            for element in data['data']:
                # Check if the current asset has already been written to the CSV file
                if element['asset'] not in assets_written:
                    # Write the current element to the CSV file
                    writer.writerow([element['asset'], element['asset_longname'], element['issuer'], element['quantity'], element['source']])
                    # Add the current asset to the set of assets that have been written to the CSV file
                    assets_written.add(element['asset'])
            # Check if there are more pages of data to retrieve
            if data['total'] > (page * page_size):
                # Increment the page number
                page += 1
            else:
                # Set the flag to indicate that there are no more pages of data to retrieve
                more_pages = False
            
            
def get_dispenses_from_assets(assets):
    # Set the field names for the CSV file
    fields = ['address', 'asset', 'block_index', 'btc_amount', 'dispenser', 'quantity', 'timestamp']

    # Open the file in write mode
    with open('csv_files/asset_disp.csv', 'w', newline='') as csvfile:
        # Create a csv.writer instance
        writer = csv.writer(csvfile)
        
        # Write the header row
        writer.writerow(fields)
        
        # Iterate over the assets in assets
        for asset in assets:
            url = 'https://xchain.io/api/dispenses/{0}'.format(asset)
    
            # Make the request to the API
            response = rq.get(url)

            new_data = response.json()['data']
            # print(new_data)
            # Iterate over the items in new_data
            for item in new_data:
                timestamp_formatted = datetime.fromtimestamp(item['timestamp'])
                
                # Write each item to the file as a separate row
                writer.writerow([item[field] for field in fields[0:-1]] + [timestamp_formatted.strftime("%Y-%m-%d %H:%M:%S")])
                # writer.writerow(timestamp_formatted.strftime("%Y-%m-%d %H:%M:%S"))
            
                
# filtering by timestamp of dispense:
def clean_dispenses_csv():
    df = pd.read_csv('csv_files/asset_disp.csv')
    df.columns = ['address', 'asset', 'block_index', 'btc_amount', 'dispenser', 'quantity', 'timestamp']
    df = df.sort_values(by=['timestamp'], ascending=False)
    df.to_csv('csv_files/asset_disp.csv')
    

def scrape_dispenses(asset_array, timestamp):
    fields = ['address', 'asset', 'block_index', 'btc_amount', 'dispenser', 'quantity', 'timestamp']
    
    # options for the url to add pagination
    endpoint = 'https://xchain.io/api/dispenses/'
    page = 0
    page_size = 100
    more_pages = True
    flag = 0
    matrix_of_values = []
    
    while more_pages:
        url = "{0}?page={1}&page_size={2}".format(endpoint, page, page_size)
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
        page+=1
        if flag == 1:
            break
    df = pd.DataFrame(matrix_of_values, columns=fields)
    old_df = pd.read_csv('csv_files/updated_asset_disp.csv')
    final_df = pd.concat([df, old_df]).drop_duplicates(subset=df.columns, keep=False, ignore_index=True)

    final_df.to_csv('csv_files/updated_asset_disp.csv', index=False)
    
    
def main():
    # reading 
    df = pd.read_csv('csv_files/issuances_df.csv')
    asset_array = df['asset'].to_numpy()
    address_to_scrape = '1DRZVQe58Tr9WxDNYdJUbye3toH1zkedX'
    timestamp_1 = '2023-02-04 21:57:21'
    datetime_obj = datetime.strptime(timestamp_1, '%Y-%m-%d %H:%M:%S')
    unix_timestamp = datetime_obj.timestamp()
    # flag to get first data from assets if the .csv files are not there:
    initialized = 0
    if not initialized:
        get_address_assets_info(address_to_scrape)
        get_dispenses_from_assets(asset_array)
        clean_dispenses_csv()
    else:
        scrape_dispenses(asset_array, unix_timestamp)

    # the code above takes a lot of time, so if i run this program every day or so,
    # it's better to get next data straight from url endpoint of api/dispenses/ until
    # we run into a block or timestamp of the last time this program was run:
    


if __name__ == "__main__":
    main()
    