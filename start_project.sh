#!/bin/bash

# Start PostgreSQL
echo "Starting PostgreSQL..."
sudo systemctl start postgresql

# Activate Django virtual environment and start backend
echo "Activating Django virtual environment and starting backend..."
source .env/bin/activate  # Adjust the path to your virtual environment
cd backend  # Replace 'backend' with your Django project folder
python manage.py runserver &
BACKEND_PID=$!

# Wait for user to terminate script
echo "Press Ctrl+C to stop the server..."
trap "kill $BACKEND_PID; deactivate; sudo systemctl stop postgresql; echo 'Servers stopped.'" INT
wait

