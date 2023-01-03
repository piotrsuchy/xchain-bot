import csv
import requests as rq

# Set the API endpoint URL
endpoint_address = 'https://xchain.io/api/issuances/'

# assets = ['CLAYWOJAK', 'XCP']
url = f'{endpoint_address}1DRZVQe58Tr9WxDNYdJUbye3toH1zkedX'

# Make the request to the API
response = rq.get(url)

# Parse the JSON data
data = response.json()

# Create a set to store the assets that have already been written to the CSV file
assets_written = set()

# Open a file for writing and create a CSV writer
with open('data.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)

    # Write the header row
    writer.writerow(['asset', 'asset_longname', 'issuer', 'quantity', 'source'])

    # Iterate over the elements in the data list
    for element in data['data']:
        # Check if the current asset has already been written to the CSV file
        if element['asset'] not in assets_written:
            # Write the current element to the CSV file
            writer.writerow([element['asset'], element['asset_longname'], element['issuer'], element['quantity'], element['source']])

            # Add the current asset to the set of assets that have been written to the CSV file
            assets_written.add(element['asset'])
