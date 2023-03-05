import requests
import csv
import json
from datetime import datetime

def save_dispense_data(asset, dispense_data, flag):
    with open('csv_files/dispenses.csv', 'a') as file:
        writer = csv.writer(file)
        if flag:
            writer.writerow(['address', 'asset', 'btc_amount', 'quantity', 'date', 'block'])
        for data in dispense_data:
            timestamp = datetime.fromtimestamp(data['timestamp'])
            writer.writerow([data['address'], asset, data.get('btc_amount', ''), data['quantity'], timestamp.strftime("%Y-%m-%d %H:%M:%S"), data['block_index']])

# Function to get dispense data for a specific address and asset
def get_dispense_data(asset):
    url = f'https://xchain.io/api/dispenses/{asset}'
    response = requests.get(url)
    if response.status_code == 200:
        dispense_data = json.loads(response.text)
        if 'error' in dispense_data:
            print(dispense_data['error'])
            return None
        else:
            return dispense_data['data']
    else:
        print(f'Error: {response.status_code}')

# Function to scrape data for a specific address and list of assets
def scrape_data(assets):
    for asset in assets:
        dispense_data = get_dispense_data(asset)
        if dispense_data:
            if asset == assets[0]:
                flag = 1
            else:
                flag = 0
            save_dispense_data(asset, dispense_data, flag)
            

assets = []
with open('csv_files/issuances_df.csv', 'r') as file:
    reader = csv.reader(file)
    for row in reader:
        assets.append(row[0])
scrape_data(assets)
