from kafka import KafkaConsumer
import json
import clickhouse_connect
from clickhouse_connect.driver.tools import insert_file
from datetime import datetime

# Kafka Configuration
KAFKA_BROKER = 'broker:9092'
KAFKA_TOPIC = 'test_topic'

# ClickHouse Configuration
CLICKHOUSE_HOST = 'clickhouse'
CLICKHOUSE_PORT = 8123
CLICKHOUSE_USER = 'myuser'
CLICKHOUSE_PASSWORD = 'mypass'
CLICKHOUSE_DATABASE = 'my_database'
CLICKHOUSE_TABLE = 'bets'


def create_table_if_not_exists(client):
    create_table_query = f"""
    CREATE TABLE IF NOT EXISTS {CLICKHOUSE_TABLE} (
        datetime DateTime,
        bets Int32,
        user_id String
    ) ENGINE = MergeTree()
    ORDER BY (datetime, user_id)
    """
    client.command(create_table_query)
    print(f"Table {CLICKHOUSE_TABLE} created or already exists.")


def insert_data(client, data):
    insert_query = f"INSERT INTO {CLICKHOUSE_TABLE} (datetime, bets, user_id) VALUES"
    client.insert(CLICKHOUSE_TABLE, data, column_names=[
                  'datetime', 'bets', 'user_id'])
    print(f"Inserted data: {data}")


def main():
    # Initialize Kafka consumer
    consumer = KafkaConsumer(
        KAFKA_TOPIC,
        bootstrap_servers=[KAFKA_BROKER],
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        group_id='clickhouse-consumer-group',
        value_deserializer=lambda x: json.loads(x.decode('utf-8'))
    )

    # Initialize ClickHouse client
    client = clickhouse_connect.get_client(
        host=CLICKHOUSE_HOST,
        port=CLICKHOUSE_PORT,
        username=CLICKHOUSE_USER,
        password=CLICKHOUSE_PASSWORD,
        database=CLICKHOUSE_DATABASE
    )

    # Create table if not exists
    create_table_if_not_exists(client)

    print(f"Starting to consume messages from {KAFKA_TOPIC}")

    # Consume messages
    for message in consumer:
        try:
            print(f"Received message: {message.value}")

            data = message.value['data']
            parsed_data = [
                (
                    datetime.strptime(data['datetime'], "%Y-%m-%d %H:%M:%S"),
                    data['bets'],
                    data['user_id']
                )
            ]
            insert_data(client, parsed_data)
        except Exception as e:
            print(f"Error processing message: {e}")
            print(f"Message: {message.value}")


if __name__ == "__main__":
    main()
