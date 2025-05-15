#!/bin/bash

# Activate your virtual environment
source .env/bin/activate

echo "Clearing pip cache..."
rm -rf ~/.cache/pip/*

echo "Clearing Python temporary files..."
find .env -type f -name "*.pyc" -delete
find .env -type d -name "__pycache__" -exec rm -r {} +

echo "Clearing system temporary files..."
sudo rm -rf /tmp/*

echo "Checking disk usage..."
df -h

echo "Cleanup complete!"
