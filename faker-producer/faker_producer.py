import os
import time
from kafka import KafkaProducer
from faker import Faker
import json
import random

KAFKA_BROKER_URL = os.environ.get("KAFKA_BROKER_URL", "localhost:9092")
TOPIC_NAME = os.environ.get("TOPIC_NAME", "fakerdata")
SLEEP_TIME = int(os.environ.get("SLEEP_TIME", 5))

fake = Faker()

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

def run():
    iterator = 0
    print("Setting up Faker producer at {}".format(KAFKA_BROKER_URL))
    producer = KafkaProducer(
        bootstrap_servers=[KAFKA_BROKER_URL],
        value_serializer=lambda x: json.dumps(x).encode('utf-8'),
    )

    while True:
        # Generate fake data
        sendit = get_faker_data()
        print(f"Sending new faker data iteration - {iterator}")
        producer.send(TOPIC_NAME, value=sendit)
        print("New faker data sent")
        time.sleep(SLEEP_TIME)
        print("Waking up!")
        iterator += 1


if __name__ == "__main__":
    run()
