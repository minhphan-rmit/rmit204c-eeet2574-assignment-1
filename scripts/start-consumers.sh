#!/bin/bash

# Script to start the consumer service

# Define the path to the consumer's docker-compose file
CONSUMER_COMPOSE_FILE="consumers/docker-compose.yml"

# Function to start the consumer service
start_consumer_service() {
    echo "Starting consumer service..."
    docker-compose -f "$CONSUMER_COMPOSE_FILE" up -d
    if [ $? -eq 0 ]; then
        echo "Consumer service started successfully."
    else
        echo "Failed to start consumer service." >&2
        exit 1
    fi
}

# Run the consumer service
start_consumer_service

echo "All consumer services are running successfully."
