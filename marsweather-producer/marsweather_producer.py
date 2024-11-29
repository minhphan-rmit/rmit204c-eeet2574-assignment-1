import os
import time
import json
import requests
from kafka import KafkaProducer

# Environment Variables
KAFKA_BROKER_URL = os.environ.get("KAFKA_BROKER_URL", "localhost:9092")
TOPIC_NAME = os.environ.get("TOPIC_NAME", "marsweather")
SLEEP_TIME = int(os.environ.get("SLEEP_TIME", 1))
BASE_URL = "https://api.nasa.gov/insight_weather/"
PARAMS = {
    "api_key": "1EUj0kjNhYsCLWlQ0ESsIhZLmHtpvmqwoQ8kVGGw",
    "feedtype": "json",
    "ver": "1.0"
}

def fetch_mars_weather():
    """
    Fetch the latest Mars weather data from NASA's InSight API.
    """
    try:
        response = requests.get(BASE_URL, params=PARAMS)
        if response.status_code != 200:
            print(f"Error fetching Mars weather from NASA API: {response.status_code} - {response.text}")
            return None
        return response.json()
    except Exception as e:
        print(f"Error during API request: {e}")
        return None


def format_weather_data(sol, weather_data):
    """
    Format Mars weather data for a specific Sol into a flat JSON structure.
    """
    try:
        formatted_data = {
            "sol": sol,
            "season": weather_data.get("Season", ""),
            "first_utc": weather_data.get("First_UTC", ""),
            "last_utc": weather_data.get("Last_UTC", ""),
            "at_avg": weather_data.get("AT", {}).get("av", None),
            "at_min": weather_data.get("AT", {}).get("mn", None),
            "at_max": weather_data.get("AT", {}).get("mx", None),
            "hws_avg": weather_data.get("HWS", {}).get("av", None),
            "hws_min": weather_data.get("HWS", {}).get("mn", None),
            "hws_max": weather_data.get("HWS", {}).get("mx", None),
            "pre_avg": weather_data.get("PRE", {}).get("av", None),
            "pre_min": weather_data.get("PRE", {}).get("mn", None),
            "pre_max": weather_data.get("PRE", {}).get("mx", None),
            "most_common_wind": weather_data.get("WD", {}).get("most_common", {}).get("compass_point", None),
        }
    except Exception as e:
        print(f"Error formatting weather data: {e}")
        formatted_data = None

    return formatted_data


def run():
    """
    Main producer loop to fetch Mars weather data and send it to Kafka.
    """
    print(f"Setting up Mars Weather producer at {KAFKA_BROKER_URL}")
    producer = KafkaProducer(
        bootstrap_servers=[KAFKA_BROKER_URL],
        value_serializer=lambda x: json.dumps(x).encode('utf-8'),
    )

    while True:
        print("Fetching Mars weather data...")
        data = fetch_mars_weather()

        if data is None:
            print("No data fetched. Retrying after sleep interval.")
            time.sleep(SLEEP_TIME)
            continue

        sol_keys = data.get("sol_keys", [])
        if not sol_keys:
            print("No Sol data available. Retrying after sleep interval.")
            time.sleep(SLEEP_TIME)
            continue

        for sol in sol_keys:
            sol_data = data.get(sol, {})
            formatted_weather = format_weather_data(sol, sol_data)

            if formatted_weather:
                print(f"Sending Mars weather data for Sol {sol}")
                producer.send(TOPIC_NAME, value=formatted_weather)
                print("Mars weather data sent.")
            else:
                print(f"Failed to format weather data for Sol {sol}")

            time.sleep(SLEEP_TIME)

if __name__ == "__main__":
    run()
