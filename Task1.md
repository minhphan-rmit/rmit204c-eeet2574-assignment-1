# EEET2574 - Big Data for Engineering

## Assignment 1: Data Pipeline with Docker

- Student: Phan Nhat Minh
- StudentID: s3978598

### Task 1: OpenWeatherMap API

In this task, I will create a OpenWeatherMap data pipleine for 2 cities: Hanoi and Ho Chi Minh City

#### Step 1: Create Docker Networks

```bash
docker network create kafka-network                         # create a new docker network for kafka cluster (zookeeper, broker, kafka-manager services, and kafka connect sink services)
docker network create cassandra-network                     # create a new docker network for cassandra. (kafka connect will exist on this network as well in addition to kafka-network)
```

#### Step 2: Verify the port is ready to use

```bash
lsof -i :<port_number>
```

On my machine, port 8081 is avilable so I will use that instead of port 7000 like in the original code, and the other ports in the original code works fine on my machine.

#### Step 3: Start Kafka and Cassandra

```bash
$ docker-compose -f cassandra/docker-compose.yml up -d
```

```bash
$ docker-compose -f kafka/docker-compose.yml up -d            # start single zookeeper, broker, kafka-manager and kafka-connect services
$ docker ps -a                                                # sanity check to make sure services are up: kafka_broker_1, kafka-manager, zookeeper, kafka-connect service
```

> **Note:** 
Kafka-Manager front end is available at http://localhost:9000

You can use it to create cluster to view the topics streaming in Kafka.


IMPORTANT: There is a bug that I don't know how to fix yet. You have to manually go to CLI of the "kafka-connect" container and run the below comment to start the Cassandra sinks.
```
./start-and-wait.sh
```