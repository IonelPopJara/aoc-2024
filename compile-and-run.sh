#!/bin/bash

# Check if a day argument is passed
if [ -z "$1" ]; then
    echo "Usage: $0 <day>"
    exit 1
fi

# Format the day into the correct file name, e.g., day-01.c
DAY=$(printf "day-%02d" "$1")

# Check if the source file exists
C_FILE="./src/$DAY/$DAY.c"
if [ ! -f "$C_FILE" ]; then
    echo "Error: Source file $C_FILE not found!"
    exit 1
fi

# Compile the C file
gcc "$C_FILE" -o "./src/$DAY/main" -g

# Run the compiled binary
./src/$DAY/main "./src/$DAY/"

