import json
import os
import pandas as pd
import requests as rq

address = input("Give the address from which you want to see the list of dispenses: ")
endpoint_address = f'https://xchain.io/api/dispenses/{address}'

response = rq.get(endpoint_address)

if response.status_code == 200:
    data = response.json()
    
    dispenses_data = data['data']
    
    # Convert the list into a Pandas DataFrame
    dispenses_df = pd.DataFrame(dispenses_data)

    # Drop unnecessary columns
    dispenses_df.drop(columns=['asset_longname', 'dispenser'], inplace=True)

    # Convert Unix timestamp to formatted date
    dispenses_df['timestamp'] = pd.to_datetime(dispenses_df['timestamp'], unit='s').dt.strftime('%d-%m-%Y')

    # Display the DataFrame
    print(dispenses_df)

    # Define the relative path to the CSV file
    current_dir = os.path.dirname(os.path.abspath(__file__))
    csv_file_path = os.path.join(current_dir, '..', 'csv_files', f'dispenses_from_{address}.csv')
    
    dispenses_df.to_csv(csv_file_path, index=False)
    print("Data saved to {}".format(csv_file_path))
    
else:
    print("Request failed with status code {}".format(response.status_code))