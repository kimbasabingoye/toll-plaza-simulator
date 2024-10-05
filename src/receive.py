#!/usr/bin/env python
from rabbitmq_helper import RabbitMQHelper
import sys
import os
import json
from dotenv import load_dotenv

load_dotenv()

GCP_PROJECT_ID = os.getenv("GCP_PROJECT_ID", "snk-labs")
TRAFFIC_GENERATOR_QUEUE_NAME = os.getenv("TRAFFIC_GENERATOR_QUEUE_NAME",
                                         "traffic_generator_queue")
RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "localhost")

print(RABBITMQ_HOST)


def process_vehicle(ch, method, properties, body):
    vehicle = json.loads(body)
    print(f" [x] Processing vehicle: {vehicle}")

    # Simulate processing time
    import time
    time.sleep(2)

    # Acknowledge the message
    ch.basic_ack(delivery_tag=method.delivery_tag)


def main():
    # Set up RabbitMQ consumer
    rabbitmq = RabbitMQHelper(queue_name=TRAFFIC_GENERATOR_QUEUE_NAME,
                              host=RABBITMQ_HOST)
    rabbitmq.consume_message(process_vehicle)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
