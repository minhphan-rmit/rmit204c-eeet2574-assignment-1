#!/bin/bash

# Script to set up Kafka and Cassandra environments

# Define network names
KAFKA_NETWORK="kafka-network"
CASSANDRA_NETWORK="cassandra-network"

# Function to create Docker networks if they don't already exist
create_network() {
    local network_name=$1
    if ! docker network ls | grep -q "$network_name"; then
        echo "Creating Docker network: $network_name"
        docker network create "$network_name"
    else
        echo "Docker network $network_name already exists."
    fi
}

# Create Kafka and Cassandra networks
create_network "$KAFKA_NETWORK"
create_network "$CASSANDRA_NETWORK"

# Start Cassandra services
echo "Starting Cassandra services..."
docker-compose -f cassandra/docker-compose.yml up -d
if [ $? -eq 0 ]; then
    echo "Cassandra services started successfully."
else
    echo "Failed to start Cassandra services." >&2
    exit 1
fi

# Start Kafka services
echo "Starting Kafka services..."
docker-compose -f kafka/docker-compose.yml up -d
if [ $? -eq 0 ]; then
    echo "Kafka services started successfully."
else
    echo "Failed to start Kafka services." >&2
    exit 1
fi

echo "Environment setup completed successfully."
