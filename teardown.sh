#!/bin/bash

# Stop visualization node
echo "Stopping visualization node..."
docker-compose -f data-vis/docker-compose.yml down

# Stop the consumers
echo "Stopping the consumers..."
docker-compose -f consumers/docker-compose.yml down

# Stop Open Weather Map producer
echo "Stopping Open Weather Map producer..."
docker-compose -f owm-producer/docker-compose.yml down

# Stop Zookeeper, broker, Kafka-manager, and Kafka-connect services
echo "Stopping Kafka cluster services..."
docker-compose -f kafka/docker-compose.yml down

# Stop Cassandra
echo "Stopping Cassandra..."
docker-compose -f cassandra/docker-compose.yml down

# Optional: Remove Kafka and Cassandra networks
read -p "Do you want to remove Kafka and Cassandra networks? (y/n): " remove_networks
if [[ "$remove_networks" == "y" ]]; then
    echo "Removing Kafka and Cassandra networks..."
    docker network rm kafka-network
    docker network rm cassandra-network
else
    echo "Skipping network removal..."
fi

# Optional: Clean up Docker resources
read -p "Do you want to clean up Docker resources (containers, volumes, images)? (y/n): " cleanup
if [[ "$cleanup" == "y" ]]; then
    echo "Removing stopped containers..."
    docker container prune -f

    echo "Removing dangling volumes..."
    docker volume prune -f

    echo "Removing all unused images..."
    docker image prune -a -f

    echo "Removing build cache..."
    docker builder prune -f

    echo "Removing all unused Docker data..."
    docker system prune -a -f
else
    echo "Skipping Docker cleanup..."
fi

echo "Teardown complete!"
