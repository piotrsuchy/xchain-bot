import os

os.system("python current_working.py")
print("Scraped & Cleaned")
os.system("column -s, -t < csv_files/address_dispenses_by_time.csv | less -S")