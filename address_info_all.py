import csv
import requests as rq

# Set the API endpoint URL
endpoint_address = 'https://xchain.io/api/issuances/'

# Set the address to retrieve issuances for
address = '1DRZVQe58Tr9WxDNYdJUbye3toH1zkedX'

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
