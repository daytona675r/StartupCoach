#!/bin/bash

# Exit on error
set -e

echo "Starting deployment script..."

# Create a virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install requirements
echo "Installing requirements..."
pip install --no-cache-dir -r requirements.txt

# Set environment variables
echo "Setting up environment..."
export PYTHONPATH=$PYTHONPATH:$(pwd)

# Start Streamlit
echo "Starting Streamlit server..."
streamlit run app.py --server.port=8000 --server.address=0.0.0.0