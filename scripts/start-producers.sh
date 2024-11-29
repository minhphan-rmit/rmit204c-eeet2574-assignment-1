#!/bin/bash

# Script to start producer services

# Function to start a Docker Compose service
start_service() {
    local service_path=$1
    local service_name=$(basename "$service_path" | sed 's/docker-compose.yml//')
    echo "Starting producer service: $service_name"
    docker-compose -f "$service_path" up -d
    if [ $? -eq 0 ]; then
        echo "Producer service $service_name started successfully."
    else
        echo "Failed to start producer service: $service_name" >&2
        exit 1
    fi
}

# Start producer services
start_service "owm-producer/docker-compose.yml"
start_service "faker-producer/docker-compose.yml"
start_service "marsweather-producer/docker-compose.yml"
start_service "neo-producer/docker-compose.yml"

echo "All producer services started successfully."