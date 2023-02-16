import os

os.system("python get_dispenses.py")
print("Scraped")
os.system("python clean_asset_disp.py")
print("Cleaned")
os.system("column -s, -t < csv_files/address_dispenses_by_time.csv | less -S")