#!/bin/bash

# Exit on error
set -e

# Check if uv is installed
if ! command -v uv &> /dev/null; then
  echo "uv is not installed. Please install it first: https://github.com/astral-sh/uv"
  exit 1
fi

# Create virtual environment and install dependencies
echo "Setting up virtual environment and installing dependencies..."
uv venv
source .venv/bin/activate
uv pip install -e .

# Copy .env_sample to .env if .env doesn't exist
if [ ! -f .env ]; then
  echo "Creating .env file from .env_sample..."
  cp .env_sample .env
  echo "Please update the .env file with your configuration."
fi

# Run database setup
echo "Setting up database..."
./scripts/setup_db.sh

echo "Development setup complete!"
echo "To start the server, run: uvicorn app.main:app --reload"