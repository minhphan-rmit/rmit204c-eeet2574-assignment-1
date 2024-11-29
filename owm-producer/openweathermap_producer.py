import asyncio
import configparser
import os
import time
from collections import namedtuple
from dataprep.connector import connect
from kafka import KafkaProducer

# Load environment variables for Kafka broker URL and topic name
KAFKA_BROKER_URL = os.environ.get("KAFKA_BROKER_URL")
TOPIC_NAME = os.environ.get("TOPIC_NAME")
SLEEP_TIME = int(os.environ.get("SLEEP_TIME"))  # Default to 60 seconds

# Load API credentials from configuration file
config = configparser.ConfigParser()
config.read('openweathermap_service.cfg')
api_credential = config['openweathermap_api_credential']
access_token = api_credential['access_token']

# Named tuple to store API credentials
ApiInfo = namedtuple('ApiInfo', ['name', 'access_token'])
apiInfo = ApiInfo('openweathermap', access_token)

# Initialize connection to the OpenWeatherMap API
sc = connect(apiInfo.name,
             _auth={'access_token': apiInfo.access_token},
             _concurrency=3)

async def get_weather(city: str):
    """
    Asynchronously fetch the weather data for a specific city using the OpenWeatherMap API.

    Args:
        city (str): The city name for which the weather data is to be fetched.

    Returns:
        DataFrame: A dataframe containing the weather data for the city.
    """
    # Query the weather API for the city
    df_weather = await sc.query("weather", q=city)
    return df_weather


def run():
    """
    Main function to run the weather data producer.
    
    It fetches weather reports for multiple cities at regular intervals, formats the data, 
    and sends it to a Kafka topic for consumption by downstream services.
    """
    # List of cities to monitor
    locations = ["Hanoi", "Ho Chi Minh City"]
    
    # Iterator to rotate through cities
    iterator = 0
    
    # Calculate the time interval for each request based on the total sleep time and number of locations
    repeat_request = SLEEP_TIME / len(locations)
    
    print("Setting up Weather producer at {}".format(KAFKA_BROKER_URL))
    
    # Initialize Kafka producer
    producer = KafkaProducer(
        bootstrap_servers=[KAFKA_BROKER_URL],
        value_serializer=lambda x: x.encode('ascii'),  # Serialize the data as ASCII
    )

    while True:
        # Rotate through the list of locations
        location = locations[(iterator + 1) % len(locations)]
        
        # Fetch current weather data for the location
        current_weather = asyncio.run(get_weather(city=location))
        
        # Add location and timestamp to the weather data
        current_weather['location'] = location
        now = time.localtime()
        current_weather['report_time'] = time.strftime("%Y-%m-%d %H:%M:%S", now)
        
        # Convert weather data to JSON format
        current_weather = current_weather.to_json(orient="records")
        
        # Slice the JSON to remove extra characters (e.g., brackets)
        sendit = current_weather[1:-1]
        
        # Log debug messages
        print(f"Sending new weather report iteration - {iterator}")
        
        # Send the weather report to Kafka topic
        producer.send(TOPIC_NAME, value=sendit)
        
        # Log message after sending data
        print("New weather report sent")
        
        # Sleep for the required interval before fetching the next report
        time.sleep(repeat_request)
        print("Waking up!")
        
        # Increment the iterator to move to the next city
        iterator += 1


if __name__ == "__main__":
    # Run the weather data producer
    run()
