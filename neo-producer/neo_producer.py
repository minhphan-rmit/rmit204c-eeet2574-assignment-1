import os
import time
import json
import requests
from kafka import KafkaProducer

# Environment Variables
KAFKA_BROKER_URL = os.environ.get("KAFKA_BROKER_URL")
TOPIC_NAME = os.environ.get("TOPIC_NAME")
SLEEP_TIME = int(os.environ.get("SLEEP_TIME"))  
BASE_URL = "https://api.nasa.gov/neo/rest/v1/feed"

def fetch_neo_data(start_date, end_date):
    """
    Fetch NEO data from NASA's NeoWS API for a specific date range.
    """
    params = {
        "start_date": start_date,
        "end_date": end_date,
        "api_key": "yES3KdGL0eyQ4zs6wIjURfqZoZxMdVkYEC8zyFMg",
    }
    try:
        response = requests.get(BASE_URL, params=params)
        if response.status_code != 200:
            print(f"Error fetching NEO data from NASA API: {response.status_code} - {response.text}")
            return None
        return response.json()
    except Exception as e:
        print(f"Error during API request: {e}")
        return None


def format_neo_data(neo):
    """
    Format NEO data into a condensed JSON structure for analysis, ensuring correct data types.
    """
    try:
        close_approach_data = neo.get("close_approach_data", [{}])[0]
        formatted_data = {
            "id": str(neo.get("id")),  # Ensure ID is a string
            "name": str(neo.get("name", "")),  # Ensure name is a string
            "close_approach_date": str(close_approach_data.get("close_approach_date", "")),  # String date
            "relative_velocity_kph": float(close_approach_data.get("relative_velocity", {}).get("kilometers_per_hour", 0.0)),  # Float
            "miss_distance_km": float(close_approach_data.get("miss_distance", {}).get("kilometers", 0.0)),  # Float
            "estimated_diameter_min_km": float(neo.get("estimated_diameter", {}).get("kilometers", {}).get("estimated_diameter_min", 0.0)),  # Float
            "estimated_diameter_max_km": float(neo.get("estimated_diameter", {}).get("kilometers", {}).get("estimated_diameter_max", 0.0)),  # Float
            "is_potentially_hazardous": bool(neo.get("is_potentially_hazardous_asteroid", False)),  # Boolean
            "orbiting_body": str(close_approach_data.get("orbiting_body", "")),  # Ensure orbiting body is a string
        }
    except Exception as e:
        print(f"Error formatting NEO data: {e}")
        return None

    return formatted_data


def run():
    """
    Main producer loop to fetch NEO data and send it to Kafka.
    """
    print(f"Setting up NEO producer at {KAFKA_BROKER_URL}")
    producer = KafkaProducer(
        bootstrap_servers=[KAFKA_BROKER_URL],
        value_serializer=lambda x: json.dumps(x).encode('utf-8'),
    )

    while True:
        # Generate the current date range (yesterday to today)
        end_date = time.strftime("%Y-%m-%d")
        start_date = time.strftime("%Y-%m-%d", time.localtime(time.time() - 86400))  # One day back

        print(f"Fetching NEO data from {start_date} to {end_date}...")
        data = fetch_neo_data(start_date, end_date)

        if data is None:
            print("No data fetched. Retrying after sleep interval.")
            time.sleep(SLEEP_TIME)
            continue

        neo_objects = data.get("near_earth_objects", {})
        if not neo_objects:
            # If no data is returned for the range, sleep for 24 hours
            print(f"No NEO data available for the range {start_date} to {end_date}. Sleeping for 24 hours...")
            time.sleep(86400)  # 24 hours in seconds
            continue

        all_data_sent = True
        for date, neo_list in neo_objects.items():
            for neo in neo_list:
                formatted_neo = format_neo_data(neo)
                if formatted_neo:
                    # Print the formatted data for verification
                    print(f"Formatted NEO data for ID {formatted_neo['id']}:")
                    print(json.dumps(formatted_neo, indent=4))

                    # Add a 5-second delay before sending each message
                    time.sleep(5)
                    
                    # Send the data to Kafka
                    print(f"Sending NEO data for ID {formatted_neo['id']} on {date}")
                    producer.send(TOPIC_NAME, value=formatted_neo)
                    print("NEO data sent.")
                else:
                    print(f"Failed to format NEO data for one object on {date}")
                    all_data_sent = False

        if all_data_sent:
            print(f"All NEO data for the range {start_date} to {end_date} has been sent.")
            print("Sleeping for 24 hours before fetching the next range...")
            time.sleep(86400)  # Sleep for 24 hours after processing all data

        print(f"Sleeping for {SLEEP_TIME} seconds...")
        time.sleep(SLEEP_TIME)


if __name__ == "__main__":
    run()
