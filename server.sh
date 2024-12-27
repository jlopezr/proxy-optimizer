#!/bin/bash

# Get the script's directory
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Go the examples directory
cd $DIR/examples

# Run the server
python3 -m http.server 8000