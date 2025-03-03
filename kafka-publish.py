from kafka import KafkaProducer
from kafka.errors import KafkaError
from datetime import datetime
import random
import json
import time
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def check_kafka_connection(bootstrap_servers):
    try:
        producer = KafkaProducer(bootstrap_servers=bootstrap_servers)
        producer.close()
        return True
    except KafkaError:
        return False

# Create a topic called "test_topic"
def create_topic(bootstrap_servers, topic_name):
    producer = KafkaProducer(bootstrap_servers=bootstrap_servers)
    producer.send(topic_name, b"{}")

def main():
    kafka_server = "broker:9092"
    check_interval = 0.1  # seconds

    # print(f"Starting Kafka server health check for {kafka_server}")
    # print(f"Checking every {check_interval} seconds")

    while True:
        # Generate a random JSON data of {"datetime": "2023-07-25 12:34:56", "bets": (any number between 1 and 100), "user_id": (any number between 1 and 1000000)}
        data = {
            "data":{
                "datetime": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "bets": random.randint(1, 100),
                # Add padding of 0 to the user_id field
                "user_id": str(random.randint(1, 1000000)).zfill(7)
            }
        }

        # Convert the data to JSON format
        json_data = json.dumps(data)

        # Publish the data to Kafka topic
        producer = KafkaProducer(bootstrap_servers=kafka_server)
        producer.send('test_topic', json_data.encode('utf-8'))

        logger.debug(f"Published data: {json_data}")

        # Wait for the specified interval before checking again
        time.sleep(check_interval)

if __name__ == "__main__":
    main()
