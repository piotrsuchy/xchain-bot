import pandas as pd
import csv
from datetime import datetime

df = pd.read_csv('csv_files/dispenses.csv')

# df = df.drop(columns=['asset_longname', 'block_index', 'tx_hash', 'dispenser'])

df.columns = ['address', 'asset_name', 'btc_amount', 'amount', 'date', 'block_id']

df = df.sort_values(by=['date'], ascending=False)

# print(df.head(10))
df.to_csv('csv_files/address_dispenses_by_time.csv')
