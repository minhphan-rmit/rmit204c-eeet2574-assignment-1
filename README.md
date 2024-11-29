# EEET2574 - Big Data for Engineering  
## Assignment 1: Data Pipeline with Docker

**Student:** Phan Nhat Minh  
**Student ID:** s3978598  

This document serves as the official documentation for **Assignment 1: Data Pipeline with Docker**. The video documentation for this assignment is available on [Youtube](https://youtu.be/E3Jw6F63wtQ).

### Acknowledgement
This project is built using resources provided by the lecturer, specifically from [this GitHub repository](https://github.com/vnyennhi/docker-kafka-cassandra). Modifications and adjustments have been made to meet the specific requirements of the assignment.

---

## Quick Installation Guide

This section provides a step-by-step guide for quickly setting up the project using bash scripts for convenience.

### Step 0: Verify Ports Availability
Before starting, ensure the required ports are available on your system. The following ports are used by the services in this project:

- **Cassandra:** 7000 (Defined in `cassandra/docker-compose.yml`)
- **Zookeeper:** 2181 (Defined in `kafka/docker-compose.yml`)
- **Broker:** 9202 (Defined in `kafka/docker-compose.yml`)
- **Kafka Manager:** 9000 (Defined in `kafka/docker-compose.yml`)
- **Kafka Connect:** 8083 (Defined in `kafka/docker-compose.yml`)
- **Data Visualization (Jupyter):** 8888 (Defined in `datavis/docker-compose.yml`)

To check if a port is in use, run the following command:

```bash
lsof -i :<port_number>
```

- If any port is occupied, update the corresponding configuration file to use a different available port. For example, if port 7000 is already in use, change it to 8081 in the respective configuration files.

### Step 1: Make Scripts Executable
Ensure that the necessary scripts are executable by running the following commands in your terminal:

```bash
chmod +x scripts/setup-kafka-cassandra.sh
chmod +x scripts/start-consumers.sh
chmod +x scripts/start-producers.sh
chmod +x scripts/start-data-vis.sh
chmod +x scripts/teardown.sh
```

### Step 2: Set Up Kafka and Cassandra
Run the setup script to configure Kafka and Cassandra.

```bash
scripts/setup-kafka-cassandra.sh
```

### Step 3: Create Kafka Cluster
Once the setup is complete, access the Kafka Manager UI by navigating to `http://localhost:9000` in your browser. Log in with the following credentials:

- **Username:** admin
- **Password:** bigbang

These credentials can be modified in the `docker-compose.yml` file in the Kafka folder.

#### Cluster Configuration:
- **Cluster Name:** mycluster
- **Cluster ZooKeeper Host:** zookeeper:2181
- Enable the following options:
  - Enable JMX Polling (Set `JMX_PORT` env variable before starting Kafka server)
  - Enable Poll consumer information (Not recommended for large numbers of consumers if ZooKeeper is used for offset tracking on older Kafka versions)
  - Enable Active OffsetCache (Not recommended for large numbers of consumers)

Click **Save** to successfully create the cluster.

### Step 4: Run Remaining Scripts
Now you can run the remaining scripts to start consumers, producers, and the data visualization environment.

```bash
scripts/start-consumers.sh
scripts/start-producers.sh
scripts/start-data-vis.sh
```

### Step 5: Resetting the Environment
To reset everything and tear down the Docker containers, use the following command:

```bash
scripts/teardown.sh
```

This will stop and remove all running containers. Be cautious when using this command as it will reset the entire environment.

---

## Manual Installation

If you prefer to run the commands manually or need to rebuild specific containers, you can follow the instructions below. Add `--build` at the end of any command to rebuild the containers.

### Step 0: Verify Ports Availability
Follow the same steps outlined in the **Quick Installation Guide** to ensure that the necessary ports are available.

### Step 1: Create Docker Networks

```bash
docker network create kafka-network          # Create network for Kafka services.
docker network create cassandra-network      # Create network for Cassandra services.
docker network ls                            # Verify network creation.
```

### Step 2: Start Cassandra and Kafka Containers
Start the Cassandra and Kafka containers using the appropriate `docker-compose.yml` files.

```bash
docker-compose -f cassandra/docker-compose.yml up -d  # Start Cassandra.
docker-compose -f kafka/docker-compose.yml up -d      # Start Kafka.
docker ps -a                                          # Check running containers.
```

### Step 3: Access Kafka Manager UI
- Open the Kafka Manager by navigating to `http://localhost:9000` in your browser.
- Log in using the credentials:
  - **Username:** admin
  - **Password:** bigbang

Once logged in, follow the steps to add a new Kafka cluster by specifying the **Cluster Name** and **Cluster Zookeeper Host**.

#### Cluster Configuration:
- **Cluster Name:** mycluster
- **Cluster ZooKeeper Host:** zookeeper:2181
- Enable the following options:
  - Enable JMX Polling (Set `JMX_PORT` env variable before starting Kafka server)
  - Enable Poll consumer information (Not recommended for large numbers of consumers if ZooKeeper is used for offset tracking on older Kafka versions)
  - Enable Active OffsetCache (Not recommended for large numbers of consumers)


### Step 4: Start Cassandra Sinks
Access the CLI of the "kafka-connect" container and execute the command to start Cassandra sinks.

```bash
./start-and-wait.sh
```

### Step 5: Start Producers
Start the necessary producers (OpenWeatherMap, Faker, TMDB) using the respective `docker-compose.yml` files.

```bash
docker-compose -f owm-producer/docker-compose.yml up -d   # Start OpenWeatherMap producer.
docker-compose -f faker-producer/docker-compose.yml up -d # Start Faker producer.
docker-compose -f marsweather-producer/docker-compose.yml up -d  # Start MarsWeather producer.
docker-compose -f neo-producer/docker-compose.yml up -d # Start NEO producer.
```

### Step 6: Start Consumers
Start the consumers to begin consuming data from Kafka topics.

```bash
docker-compose -f consumers/docker-compose.yml up -d     # Start Kafka consumers.
```

### Step 7: Querying Data in Cassandra
Log into the Cassandra container and use CQL (Cassandra Query Language) to query the necessary tables for the weather data, fake data, and movie data.

```bash
docker exec -it cassandra bash                        # Access Cassandra container.
```

```bash
$ cqlsh --cqlversion=3.4.4 127.0.0.1                   # Make sure you use the correct cqlversion
cqlsh> desc keyspaces;                                 # View databases.
cqlsh> use kafkapipeline;                              # Switch to kafkapipeline keyspace.
cqlsh> desc tables;                                    # View tables.
cqlsh:kafkapipeline> select * from weatherreport;      # Query data from weatherreport table.
cqlsh:kafkapipeline> select * from fakerdata;          # Query data from fakerdata table.
cqlsh:kafkapipeline> select * from movies;             # Query data from movies table.
```


### Step 8: Data Visualization
Start the Jupyter notebook for data visualization by running the appropriate command. Once the container is running, navigate to `http://localhost:8888` to access the notebook.

```bash
docker-compose -f data-vis/docker-compose.yml up -d  # Start Jupyter Notebook.
```

### Step 9: Teardown
To stop all running Kafka cluster services, execute the respective `docker-compose.yml down` commands for each service:

To stop all running kakfa cluster services:
```bash
docker-compose -f data-vis/docker-compose.yml down                  # Stop visualization
docker-compose -f consumers/docker-compose.yml down                 # Stop consumers
docker-compose -f owm-producer/docker-compose.yml down              # Stop owm producer
docker-compose -f faker-producer/docker-compose.yml down            # Stop faker producer
docker-compose -f marsweather-producer/docker-compose.yml down      # Stop tmdb producer
docker-compose -f neo-producer/docker-compose.yml down              # Stop neo producer
docker-compose -f kafka/docker-compose.yml down                     # Stop kafka
docker-compose -f cassandra/docker-compose.yml down             # Stop cassandra
```
To remove the kafka and cassandra network:
```bash
docker network rm kafka-network            # Remove kafka network
docker network rm cassandra-network        # Remove cassandra network
```

Finally, remove any unused Docker networks and resources to clean up your environment.

```bash
docker container prune    # Remove stopped containers
docker volume prune       # Remove all volumes
docker image prune -a     # Remove all images
docker builder prune      # Remove all build cache
docker system prune -a    # Remove everything
```

---

## Conclusion

This guide outlines the installation and configuration of a Kafka-based data pipeline for real-time data ingestion and processing using Docker. By following these instructions, you can successfully set up a Kafka and Cassandra environment, start producers and consumers, and visualize the data with Jupyter notebooks.

Feel free to reach out if you encounter any issues or have further questions!

---

## Assignment Fulfillment

### Task 1: OpenWeatherMap

For **Task 1**, I registered for an API key from the [OpenWeatherMap API](https://openweathermap.org/api) to access real-time weather data.

Following the steps in the tutorial from the provided [GitHub repo](https://github.com/vnyennhi/docker-kafka-cassandra), I made the following adjustments:
- Updated the API key in the `owm-producer/openweathermap_service.cfg` file.
- Checked the [OpenWeatherMap city list](https://openweathermap.org/storage/app/media/cities_list.xlsx) and selected **Hanoi** and **Ho Chi Minh City**.
- Replaced `["Vancouver"]` with `["Hanoi", "Ho Chi Minh City"]` in the `owm-producer/openweathermap_producer.py` file.

Finally, I cleaned up the code by adding meaningful comments and appropriate spacing. This concludes the completion of **Task 1**.

---

### Task 2: Faker API

For **Task 2**, I used the [Faker API](https://faker.readthedocs.io/en/master/providers.html) to simulate financial portfolio data for customer evaluation. Instead of choosing random fields, I developed a scenario for **financial portfolio analysis**. The selected fields simulate the following customer data:

- Personal Information: Name, SSN, Job, Age, Gender
- Financial Information: Income, Credit Card Provider, Credit Card Number, Expiration Date, Security Code
- Address: City, Country, Postcode, Street Name
- Spending Patterns: Monthly Purchases, Average Purchase Amount

```python
def get_faker_data():
    return {
        # Personal Information
        "name": fake.name(),
        "ssn": fake.ssn(),
        "job": fake.job(),
        "age": random.randint(18, 70),
        "gender": random.choice(["Male", "Female"]),
        # Financial Information
        "income": random.randint(30000, 200000),  # Annual income in USD
        "credit_card_provider": fake.credit_card_provider(),
        "credit_card_number": fake.credit_card_number(),
        "credit_card_expire": fake.credit_card_expire(),
        "credit_card_security_code": fake.credit_card_security_code(),
        # Address
        "city": fake.city(),
        "country": fake.country(),
        "postcode": fake.postcode(),
        "street_name": fake.street_name(),
        # Spending Patterns
        "monthly_purchases": random.randint(0, 50),
        "avg_purchase_amount": round(random.uniform(5, 500), 2),  # Average amount per purchase
    }
```

I followed the tutorial's steps to set up the producer and consumer, conducted analysis on the generated data, and documented it in the Jupyter notebook located at `data-vis/python/financial_portfolio_analysis.ipynb`. Additionally, I refined the code by cleaning and adding comments, fulfilling **Task 2**.

---

### Task 3: Integrating NASA APIs

For **Task 3**, I chose to integrate two **NASA APIs** into the Kafka pipeline. These APIs are relevant for space exploration and planetary defense:

1. **Mars Weather API**: Provides real-time Martian atmospheric data, essential for supporting space missions, rover operations, and future human exploration on Mars.
2. **NeoWs (Near Earth Object Web Service)**: Provides data on near-Earth objects (NEOs), which is vital for planetary defense and understanding the potential risks posed by asteroids or comets.

You can access [NASA API Website](https://api.nasa.gov/) to register your API key and browse for more APIs.

Here is the detailed information of these APIs:

---

#### 1. **Mars Weather API**

The **Mars Weather API** provides real-time data about the atmospheric conditions on Mars. This data is crucial for scientists and engineers working on Mars missions, as it helps to monitor weather patterns and adjust mission plans for rover operations, lander activities, and future human exploration of Mars.

##### Key Features:
- **Source**: The data comes from NASA's Curiosity rover and other Mars surface missions, which are equipped with sensors that measure temperature, wind speed, atmospheric pressure, and dust conditions on the Martian surface.
  
- **Data Points Provided**:
  - **Temperature**: Daily maximum, minimum, and average temperatures measured in degrees Celsius.
  - **Wind Speed**: Maximum and average wind speeds.
  - **Pressure**: Atmospheric pressure on the surface of Mars.
  - **Humidity**: Relative humidity levels on Mars, although it is typically very low compared to Earth.
  - **Dust**: Information on dust storms or dust-related events that can affect rover operations.
  
- **API Endpoints**:
  - **/weather**: Returns the daily weather data from the Curiosity rover, such as temperature, wind, pressure, and more.
  - **/sol**: Data on Martian days, known as "sols", providing weather conditions on a specific day or period of interest.
  
- **Applications**:
  - **Space Missions**: Supports NASA's rovers and landers, ensuring they operate in optimal conditions based on Martian weather data.
  - **Rover Operations**: Helps engineers plan rover movements and activities by predicting dust storms and extreme temperature conditions.
  - **Human Exploration**: Essential data for planning future human missions to Mars, including habitat construction, astronaut health, and life support systems.
  
- **Key Takeaway**: The Mars Weather API provides real-time and historical atmospheric data, which is crucial for mission planning, rover performance, and future Mars colonization efforts.

#### 2. NeoWs (Near-Earth Object Web Service) API Integration

The **NeoWs (Near-Earth Object Web Service)** provides data on Near-Earth Objects (NEOs), such as asteroids and comets, that pass near Earth. These objects are a potential hazard to Earth, so monitoring their size, trajectory, and proximity is vital for planetary defense. The API offers access to up-to-date information on NEOs that could potentially collide with Earth, as well as tracking known objects over time.

##### Key Features:
- **Source**: The data is collected from NASA’s NEO Observations Program, which monitors and catalogs objects that are within 1.3 astronomical units (AU) of Earth. This includes real-time observation data, as well as historical data on past NEO encounters.
  
- **Data Points Provided**:
  - **NEO Name**: The name or identifier of the object.
  - **Estimated Size**: Diameter of the NEO, in meters, along with its uncertainty.
  - **Orbit Data**: Includes the object's orbit, velocity, and its potential risk level (e.g., the likelihood of collision with Earth).
  - **Close Approach Data**: The closest approach date, distance from Earth, and speed at which the object is traveling.
  - **Impact Risk**: A "hazard" rating based on the likelihood of an Earth impact.
  
- **API Endpoints**:
  - **/neo/rest/v1/feed**: Returns a feed of NEOs that are approaching Earth within a given timeframe (e.g., daily, weekly).
  - **/neo/rest/v1/neo/{id}**: Returns detailed information on a specific NEO using its unique ID.
  - **/neo/rest/v1/neo/{id}/close_approach_data**: Returns data about the object's close approach to Earth.
  - **/neo/rest/v1/neo/{id}/hazardous**: Indicates if the NEO is considered hazardous.
  
- **Applications**:
  - **Planetary Defense**: The data is crucial for planetary defense efforts by identifying and tracking potentially hazardous NEOs to assess the risk of Earth impact.
  - **Space Research**: Researchers can study NEOs' characteristics, composition, and trajectories to understand their formation and behavior.
  - **Public Awareness**: Provides transparency in tracking near-Earth objects and their potential threat to Earth, helping to inform decision-making and policy.
  
- **Key Takeaway**: NeoWs provides detailed tracking and analysis of Near-Earth Objects, offering critical data for planetary defense and scientific research on the nature of asteroids and comets.

--- 

I followed similar steps as in **Task 2** to integrate these APIs, including:
- Creating schema in Cassandra,
- Setting up Kafka producers and consumers,
- Adjusting Cassandra utilities for data visualization.

Both APIs were successfully integrated and are showcased in the video documentation.

---

### Task 4: Visualization and Analysis

For **Task 4**, I provided at least two meaningful visualizations and analyses based on the data from the integrated APIs. These are stored in the Jupyter notebook located in `data-vis/python/`, where I presented insights from the weather data, financial portfolio analysis, and asteroid tracking data.

In this task, due to time limit, I can only conduct some brief analysis instead of only visualization for other APIs, here are some interesting findings when analyse the weather data on Mars using the Mars Weather API:

#### Summary of Mars Weather Data Analysis

In this analysis, we examined the weather data from Mars, focusing on key atmospheric variables such as temperature, wind speed, and atmospheric pressure over the latest 6 sols. Below is a brief summary of the findings:

1. **Average Atmospheric Temperature**:
   - The Martian temperature (`at_avg`) consistently remained low, averaging around **-62.5°C**, with a slight fluctuation between **-63°C** and **-61°C**. This reflects Mars' cold environment and seasonal changes.
   - The **maximum temperature** reached around **-13°C**, while the **minimum temperature** plummeted to approximately **-97°C**, highlighting the extreme temperature variations between day and night.

2. **Wind Speed**:
   - The average **horizontal wind speed** (`hws_avg`) ranged between **5.25 m/s** and **8.5 m/s**, with **max wind speeds** reaching up to **26.9 m/s**. These wind patterns show moderate to strong winds that could be associated with dust storms or other atmospheric phenomena.
   - **Minimum wind speeds** were as low as **0.23 m/s**, indicating calm periods in the Martian atmosphere.

3. **Atmospheric Pressure**:
   - The **average atmospheric pressure** (`pre_avg`) fluctuated between **746 Pa** and **750 Pa**, with the **maximum** pressure reaching up to **768 Pa** and the **minimum** pressure around **717 Pa**.
   - These fluctuations in pressure suggest that Mars experiences dynamic atmospheric conditions, which may be tied to Martian weather systems or seasonal variations.

4. **General Trends**:
   - Over the 6 sols, there was a slight **increase in pressure** and **moderate wind speeds**. The data shows typical Martian weather characteristics, with cold temperatures, significant day-night temperature variation, and variable wind conditions.

In conclusion, the Martian atmosphere shows a dynamic yet predictable pattern, with fluctuations in temperature, wind speed, and pressure reflecting seasonal shifts and possible weather phenomena.

---

### Practical Implication of the Project

This project is designed to build a robust data pipeline that integrates diverse real-time APIs to provide valuable insights across multiple domains, including weather data, financial portfolio analysis, and planetary science. By leveraging **Kafka**, **Cassandra**, and **Python**, the pipeline collects, processes, and stores data from multiple sources, enabling efficient analysis, decision-making, and predictive modeling.

#### Use Case and Scenario

##### Weather Data for Multiple Cities
The integration of the **OpenWeatherMap API** enables real-time weather data collection for cities like **Hanoi** and **Ho Chi Minh City**. This data is essential for:
- Weather forecasting,
- Disaster management,
- Climate change monitoring.

Local authorities or meteorological agencies can use this data to predict severe weather events, plan disaster responses, and optimize resource allocation.

##### Financial Portfolio Analysis
Using the **Faker API**, I simulated detailed financial profiles (income, credit score, spending patterns, etc.) to support portfolio managers in evaluating customer behavior. This data can be used to:
- Build credit scoring models,
- Detect fraud,
- Offer personalized financial services.

Financial institutions can use this simulated data to experiment with models, assess risk, and enhance customer segmentation.

##### Planetary Defense and Space Exploration
The integration of **NASA's NeoWs** and **Mars Weather API** offers valuable data for:
- **Planetary defense**: Monitoring and tracking near-Earth asteroids to assess potential risks of collision.
- **Space exploration**: Providing real-time Martian weather conditions to support ongoing missions and human exploration on Mars.

These APIs contribute to the monitoring of potential asteroid threats and the design of future space missions.

#### How the Approach Helps Solve Problems

##### Improved Decision-Making and Forecasting
Real-time weather insights help authorities make informed decisions during severe weather events. Cities can issue timely warnings, and governments can allocate resources to areas at risk. The flexibility to scale the pipeline by adding more cities or parameters further enhances decision-making.

##### Efficient Financial Analysis
By using simulated data, financial institutions can quickly build and test customer analysis tools without the need for sensitive real data. This approach allows:
- Rapid development of credit scoring systems,
- Testing fraud detection models,
- Offering targeted financial products.

Simulated data serves as a foundation for more sophisticated models, leveraging machine learning for fraud detection and customer segmentation.

##### Planetary Defense and Space Exploration
The integration of **NASA's APIs** helps assess asteroid risks and supports space missions by monitoring Martian weather. These data points help:
- Space agencies develop planetary defense strategies,
- Guide the design of Mars habitats and rover operations,
- Track asteroid trajectories for potential mitigation strategies.

#### Conclusion

By integrating **OpenWeatherMap**, **Faker**, and **NASA APIs**, this project connects diverse domains — weather forecasting, financial analysis, and planetary science. The pipeline provides essential data to businesses, governments, and space agencies, supporting better decision-making and innovation. The ability to aggregate and analyze data from various sources effectively addresses global challenges like climate change, financial risk management, and planetary defense.
