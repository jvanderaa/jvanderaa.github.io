#!/bin/bash

# Ensure poetry is installed
if ! command -v poetry &> /dev/null
then
    echo "Poetry could not be found, please install it first."
    exit
fi

# Generate requirements.txt from poetry
poetry export -f requirements.txt --output requirements.txt --without-hashes
