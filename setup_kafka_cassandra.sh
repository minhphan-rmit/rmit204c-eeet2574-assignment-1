#!/bin/bash

# Create Docker networks
echo "Creating Docker networks..."

if ! docker network inspect kafka-network &>/dev/null; then
    echo "Creating kafka-network..."
    docker network create kafka-network
else
    echo "kafka-network already exists."
fi

if ! docker network inspect cassandra-network &>/dev/null; then
    echo "Creating cassandra-network..."
    docker network create cassandra-network
else
    echo "cassandra-network already exists."
fi

# Start Cassandra
echo "Starting Cassandra..."
docker-compose -f cassandra/docker-compose.yml up -d

# Start Kafka
echo "Starting Kafka services..."
docker-compose -f kafka/docker-compose.yml up -d

echo "Setup complete!"
