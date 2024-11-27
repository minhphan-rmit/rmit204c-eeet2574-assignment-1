# EEET2574 - Big Data for Engineering

## Assignment 1: Data Pipeline with Docker

### Pre-requisites
Ensure your machine has the following pre-requisites:
- `docker` and `docker-compose` installed and operational.

**Note:** Adjustments may be required for MacOS Sequoia and Apple Silicon Chip compatibility.

---

### Task 1: OpenWeatherMap API for Hanoi and Ho Chi Minh City

#### Step 1: Make the Scripts Executable
Ensure the required scripts are executable by running these commands:

```bash
chmod +x setup_kafka_cassandra.sh
chmod +x teardown.sh
```

#### Step 2: Verify Ports Availability
Check if the necessary ports are available for the project. The ports used in the original project are:

- **Cassandra**: 7000 (defined in `cassandra/docker-compose.yml`)
- **Zookeeper**: 2181 (defined in `kafka/docker-compose.yml`)
- **Broker**: 9202 (defined in `kafka/docker-compose.yml`)
- **Kafka Manager**: 9000 (defined in `kafka/docker-compose.yml`)
- **Kafka Connect**: 8083 (defined in `kafka/docker-compose.yml`)
- **Data Visualization**: 8888 (defined in `datavis/docker-compose.yml`)

Use the following command to verify whether a specific port is in use:

```bash
lsof -i :<port_number>
```

If any port is occupied, update the configuration files to use a different available port. For example, if Cassandra's port is occupied, you can change it to 8081.

#### Step 3: Setup Kafka and Cassandra
Run the script to initialize Kafka and Cassandra:

```bash
./setup_kafka_cassandra.sh
```

#### Step 4: Create a New Kafka Cluster
1. Open a CLI for the `kafka_connect` container and run:

   ```bash
   ./start-and-wait.sh
   ```

2. Access the Kafka Manager Interface at [http://localhost:9000](http://localhost:9000).
3. Create a new cluster with the following details:
   - **Cluster Name**: `mycluster`
   - **Zookeeper Version**: (Specify the appropriate version.)
   - Enable additional options as needed.

#### Step 5: Update Target Cities in the OpenWeatherMap Producer
To fetch weather data for Hanoi and Ho Chi Minh City, perform the following:

1. Verify the city names are supported by the OpenWeatherMap API by consulting the city list: [Download city list](https://openweathermap.org/storage/app/media/cities_list.xlsx).
2. Edit the `openweathermap_producer.py` file, replacing any existing cities in the list with:

   ```python
   cities = ["Hanoi", "Ho Chi Minh City"]
   ```

3. Add your OpenWeatherMap API key to the `openweathermap_service.cfg` file.

#### Step 6: Start the Producer
Start the OpenWeatherMap producer with the following command:

```bash
docker-compose -f owm-producer/docker-compose.yml up -d
```

#### Step 7: Start the Consumer
Run the consumer with the following command:

```bash
docker-compose -f consumers/docker-compose.yml up
```

#### Step 8: Verify Data in Cassandra
To confirm that data is arriving in Cassandra:

1. Log into the Cassandra container:

   ```bash
   docker exec -it cassandra bash
   ```

2. Open `cqlsh` and query the relevant tables:

   ```bash
   cqlsh --cqlversion=3.4.4 127.0.0.1
   
   cqlsh> use kafkapipeline;  # Use the correct keyspace name
   
   cqlsh:kafkapipeline> select * from weatherreport;
   ```

#### Step 9: Data Visualization
Start the data visualization service with the following command:

```bash
docker-compose -f datavis/docker-compose.yml up -d
```

Access the visualization notebook at [http://localhost:8888](http://localhost:8888). Use the notebook to analyze and visualize the data.

#### Step 10: Tear Down
To stop all services and clean up the environment, use the teardown script:

```bash
./teardown.sh
```

---

### Additional Comments
- Make sure to troubleshoot any issues arising from port conflicts or container permissions.
- Keep your API keys and sensitive information secure and do not expose them in public repositories.
- Always stop and clean up your Docker containers to free up resources after completing the assignment.
