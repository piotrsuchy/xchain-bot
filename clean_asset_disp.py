import pandas as pd
import csv
from datetime import datetime

df = pd.read_csv('csv_files/asset_disp.csv')

df = df.drop(columns=['asset_longname', 'block_index', 'tx_hash', 'dispenser'])

df = df.sort_values(by=['timestamp'], ascending=False)

# Convert the timestamp column from Unix timestamp to a human-readable date
df['date'] = df['timestamp'].apply(lambda x: datetime.utcfromtimestamp(x).strftime('%Y-%m-%d %H:%M:%S'))
df = df.drop(columns=['timestamp'])
# y = df['date']

# df['date'] = datetime.utcfromtimestamp(y).strftime('%Y-%m-%dT%H:%M:%SZ')

# df = df.sort_values(by=['btc_amount'], ascending=False)

# print(df.head(10))
df.to_csv('csv_files/address_dispenses_by_time.csv')
