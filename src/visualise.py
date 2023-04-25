import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as ticker
import os
import mplcursors

def format_tooltip(sel):
    sel.annotation.set_text(f'Timestamp: {mdates.num2date(sel.target[0]).strftime("%Y-%m-%d %H:%M:%S")}\nBTC Amount: {sel.target[1]:.5f}')

asset_name = input("Enter the name of the asset that you want to plot: ")
creator_address = input("Enter the address of the creator of that asset: ")

# Define the relative path to the CSV file
current_dir = os.path.dirname(os.path.abspath(__file__))
csv_file_path = os.path.join(current_dir, '..', 'csv_files', f'asset_dispenses_{creator_address}.csv')

if not os.path.exists(csv_file_path):
    print("No info about the creator of this asset. To visualise, scrape that address first!")
else: 
    # Read the CSV data from a file
    data = pd.read_csv(csv_file_path, parse_dates=['timestamp'])

    # Filter the data based on the 'asset' column
    filtered_data = data[data['asset'] == asset_name]

    if filtered_data.empty:
        print("This asset was not created by that address, or hasn't had any dispenses yet!")
    else:
        # Filter the data based on the 'asset' column
        filtered_data = data[data['asset'] == asset_name].copy()

        # Calculate the unit BTC amount before expanding the DataFrame
        filtered_data['unit_btc_amount'] = filtered_data['btc_amount'] / filtered_data['quantity']

        # Expand the DataFrame based on the 'quantity' value
        expanded_data = filtered_data.loc[filtered_data.index.repeat(filtered_data['quantity'])].reset_index(drop=True)

        # Update the 'btc_amount' and 'quantity' columns
        expanded_data['btc_amount'] = expanded_data['unit_btc_amount']
        expanded_data['quantity'] = 1
        
        # Plot the graph
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(expanded_data['timestamp'], expanded_data['btc_amount'], marker='o', linestyle='-', label=asset_name)

        # Format the X-axis with only the first and last date
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        ax.xaxis.set_major_locator(ticker.MaxNLocator(2))
        plt.xticks(rotation=45)

        # Set labels and title
        plt.xlabel('Timestamp')
        plt.ylabel('Unit BTC Amount')
        plt.title('Unit BTC Amount for {}'.format(asset_name))

        # Add a legend
        plt.legend()

        # Enable mplcursors for interactive hovering
        mplcursors.cursor().connect('add', format_tooltip)
        mplcursors.cursor(hover=True)

        # Show the plot
        plt.show()