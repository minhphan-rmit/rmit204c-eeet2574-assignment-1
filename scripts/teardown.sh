#!/bin/bash

# Script to teardown all services and clean Docker cache

echo "Stopping all services and cleaning Docker resources..."

# Function to stop all running Docker Compose services
stop_services() {
    echo "Stopping all Docker Compose services..."
    docker-compose -f cassandra/docker-compose.yml down
    docker-compose -f kafka/docker-compose.yml down
    docker-compose -f owm-producer/docker-compose.yml down
    docker-compose -f faker-producer/docker-compose.yml down
    docker-compose -f marsweather-producer/docker-compose.yml down
    docker-compose -f neo-producer/docker-compose.yml down
    docker-compose -f consumers/docker-compose.yml down
    echo "All Docker Compose services stopped."
}

# Function to remove Docker networks
remove_networks() {
    echo "Removing Docker networks..."
    docker network rm kafka-network cassandra-network 2>/dev/null
    echo "Docker networks removed."
}

# Function to clean Docker resources
clean_docker() {
    echo "Cleaning Docker resources..."

    # Remove stopped containers
    docker container prune -f

    # Remove unused images
    docker image prune -af

    # Remove unused volumes
    docker volume prune -f

    # Remove unused networks
    docker network prune -f

    echo "Docker resources cleaned."
}

# Main script execution
stop_services
remove_networks
clean_docker

echo "Teardown completed. Docker environment is clean."
