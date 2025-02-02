#!/bin/bash

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "Creating .env file..."
    echo "SECRET_KEY=$(openssl rand -hex 32)" > .env
    echo "OPENAI_API_KEY=your-openai-api-key" >> .env
fi

# Start the services
docker compose up --build 