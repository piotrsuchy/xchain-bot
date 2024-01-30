#!/opt/homebrew/bin/bash

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

read -p "What asset dispenses would you like to see? `echo $'\n> '`" asset_name

echo "Grepping through dispenses.txt for ${asset_name}"
grep ${asset_name} "${SCRIPT_DIR}/../dispenses.txt"
