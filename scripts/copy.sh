#!/bin/bash

# Set the source and destination directories
source_dir=/app
destination_dir=/config

# Get a list of files in the source directory
files=$(ls "$source_dir")

# Loop through the list of files
for file in $files
do
  # Check if the file exists in the destination directory
  if [ ! -f "$destination_dir/$file" ]; then
    # If the file does not exist, copy it to the destination directory
    cp "$source_dir/$file" "$destination_dir/$file"
    echo "Copied $file to $destination_dir"
  else
    echo "$file already exists in $destination_dir"
  fi
done
