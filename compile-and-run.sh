#!/bin/bash

# Check if a day argument is passed
if [ -z "$1" ]; then
    echo "Usage: $0 <day>"
    exit 1
fi

# Format the day into the correct file name, e.g., day-01
DAY=$(printf "day-%02d" "$1")

# Check if the source file exists
C_FILE="./src/$DAY/$DAY.c"
PY_FILE="./src/$DAY/$DAY.py"

if [ -f "$C_FILE" ]; then
    # Compile the C file
    gcc "$C_FILE" -o "./src/$DAY/main" -g
    # Run the compiled binary
    ./src/$DAY/main "./src/$DAY/"
elif [ -f "$PY_FILE" ]; then
    python "$PY_FILE" "./src/$DAY/"
else
    echo "Error: Source file not found!"
fi

exit 1



