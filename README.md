# Kafka Clickhouse Integration

## Overview
This project demonstrates a data pipeline that generates JSON data, sends it to a Kafka topic, and then saves the data to ClickHouse for efficient storage and analysis.

## What's inside - Understanding `docker-compose.yml`

The `docker-compose.yml` file defines the following services:

1. **Network**: `kafka-cilckhouse-network` - Custom network for inter-service communication.
2. `datagenerator`: Generate random JSON data and publish to Kafka.
3. `dataconsumer`: Consume messages from Kafka and insert into ClickHouse.

4. **(Kafka) Broker**: The main Kafka service for message streaming.
   - Image: apache/kafka
   - Port:
     - 9092 (internal)
     - 8083 (For Kafka Connect REST API)
     - 8085
     - 9997

9. **Kafka UI**: Another web interface for Kafka management.
   - Image: provectuslabs/kafka-ui:latest
   - Port: 8080

7. **ClickHouse**: Column-oriented database for data storage and analysis.
   - Image: clickhouse/clickhouse-server
   - Ports: 8123 (HTTP), 9000 (native TCP)

6. **ClickHouse UI**: Web interface for ClickHouse management.
   - Image: ghcr.io/caioricciuti/ch-ui
   - Port: 5521

## Setup and Usage

1. Ensure Docker and Docker Compose are installed on your system.
2. Clone this repository to your local machine.
3. Navigate to the project directory.
4. Run `docker-compose up -d` to start all services in detached mode.
5. Wait for all services to initialize (this may take a few minutes).

## Components

### Kafka Publisher (`kafka-publish.py`)

This script generates random JSON data and publishes it to a Kafka topic named 'test_topic'. It includes:
- Random data generation (datetime, bets, user_id)
- Kafka producer setup
- Continuous data publishing with a configurable interval

### Kafka Consumer (`kafka-consume.py`)

This script consumes messages from the Kafka topic and inserts them into ClickHouse. It includes:
- Kafka consumer setup
- ClickHouse client initialization
- Table creation in ClickHouse (if not exists)
- Data parsing and insertion into ClickHouse

## Accessing Services

- Kafka UI: http://localhost:8080
- ClickHouse UI: http://localhost:5521

## Dependencies

The project uses the following main Python libraries:
- kafka-python: For Kafka producer and consumer operations
- clickhouse-connect: For interacting with ClickHouse

Install the dependencies using:

`pip install -r requirements.txt`

## Monitoring and Management

Use the Kafka UI to monitor topics, consumers, and overall Kafka cluster health. You can execute ClickHouse queries directly through its HTTP interface to verify data insertion and perform analysis, or using the ClickHouse web UI to access a more user-friendly interface.

## Notes

- Ensure all services are healthy before running the Python scripts.
- Adjust the data generation rate in `kafka-publish.py` if needed.
- Monitor ClickHouse insertion performance and adjust batch sizes if necessary.
- You can start Kafka service and ClickHouse service/UI services first.
  - Then start `datagenerator` to start generate and sending data to Kafka.
  - Finally, start `dataconsumer` to consume data from Kafka and insert into ClickHouse.