import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as ticker
import os
import mplcursors

# TODO: take into account multiple dispenses and divide the btc amount by dispenses
# TODO: change the csv_file_path based on asset_name

def format_tooltip(sel):
    sel.annotation.set_text(f'Timestamp: {mdates.num2date(sel.target[0]).strftime("%Y-%m-%d %H:%M:%S")}\nBTC Amount: {sel.target[1]:.5f}')

mplcursors.cursor().connect('add', format_tooltip)

# Define the relative path to the CSV file
current_dir = os.path.dirname(os.path.abspath(__file__))
csv_file_path = os.path.join(current_dir, '..', 'csv_files', 'asset_dispenses_1DRZVQe58Tr9WxDNYdJUbye3toH1zkedX.csv')

# Read the CSV data from a file
data = pd.read_csv(csv_file_path, parse_dates=['timestamp'])

# Filter the data based on the 'asset' column
asset_name = 'DAILYSMOL'
filtered_data = data[data['asset'] == asset_name]

# Plot the graph
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(filtered_data['timestamp'], filtered_data['btc_amount'], marker='o', linestyle='-', label=asset_name)

# Format the X-axis with only the first and last date
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
ax.xaxis.set_major_locator(ticker.MaxNLocator(2))
plt.xticks(rotation=45)

# Set labels and title
plt.xlabel('Timestamp')
plt.ylabel('BTC Amount')
plt.title('BTC Amount for {}'.format(asset_name))

# Add a legend
plt.legend()

# Enable mplcursors for interactive hovering
mplcursors.cursor(hover=True)

# Show the plot
plt.show()
