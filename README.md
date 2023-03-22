# Description:

This project is a simple terminal app (with some bash scripts) that based on input will give you information from the https://xchain.io blockchain - Counterparty Blockchain (XCP token). As someone who used that blockchain and website I've found the tools to find certain information not sufficient so I decided to code something up to remedy it.

I've focused on dispenses from a certain address. By entering the address you will get a .csv file that contains most of the interesting information (will be customizable in the future) about the dispense. Some more work is needed to clean the data and perhaps visualise the trends for specific assets, but at the very least the program is working. I recommend using the scripts in /scripts folder for the best experience. Second command below might be necessary to change the permissions right after downloading from the repo. This sets the execute permission bit (x) for the owner (u - skip this if you want to set the execute permission for all users) of the file. Run them by:

```bash
$ cd scripts/
$ chmod u+x xchain_insert_address.sh
$ ./xchain_insert_address
```


## Example:

### For input:

![example_input](media/example_input.png)

### We get the following output after running the script:

![example_output](media/example_output.png)

As you can see we get the information about dispenses in a nice format (actually a .csv file).

## Useful links to get more information about the blockchain and XCP:

- https://xchain.io/
- https://dankset.io/
- https://www.blockchain.com/explorer