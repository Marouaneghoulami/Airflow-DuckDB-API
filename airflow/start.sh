#!/bin/bash

# Set the PYTHONPATH to include the dags directory
export PYTHONPATH="$(pwd)/dags:$PYTHONPATH"

# Execute the Python file
echo "Running init-db.py script..."
python dags/setup/database_manager.py

# Check if the Python script ran successfully
if [ $? -ne 0 ]; then
  echo "Python script failed. Exiting."
  exit 1
fi

# Run Docker Compose with --build
#echo "Starting Docker Compose with build..."
#docker-compose up --build
