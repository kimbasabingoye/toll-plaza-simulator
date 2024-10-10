
import enum
import os
import json

import dotenv
from google.cloud import pubsub_v1
import pika

dotenv.load_dotenv()

PROJECT_ID = os.getenv("GCP_PROJECT_ID", "")
QUEUE_NAME = os.getenv("QUEUE_NAME", "")
RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "")

class MessagingSystem(str, enum.Enum):
    """Class representing the messaging system to use to send
    vehicle processing information"""
    STDOUT = "standard_output"
    RABBITMQ = "rabbit_mq"
    PUBSUB = "pub_sub"

class MessageSender:
    def __init__(self, message_sender_system: MessagingSystem = MessagingSystem.STDOUT) -> None:
        self.messaging_system = message_sender_system

    def send_message(self, message: str):
        """Send message using the setted message sender system"""
        sender = self._get_sender(self.messaging_system)
        sender(message)

    def _get_sender(self, messaging_system: MessagingSystem):
        if messaging_system == MessagingSystem.STDOUT:
            return self._print_message
        elif messaging_system == MessagingSystem.RABBITMQ:
            return self._send_to_rabbitmq
        elif messaging_system == MessagingSystem.PUBSUB:
            return self._send_to_pubsub
        else:
            raise ValueError(messaging_system)

    def _print_message(self, message):
        print(f"{message}")

    def _send_to_rabbitmq(self, message):
        connection = None
        try:
            connection = pika.BlockingConnection(
                pika.ConnectionParameters(host=RABBITMQ_HOST))
            channel = connection.channel()
            channel.queue_declare(queue=QUEUE_NAME, durable=True)
            channel.basic_publish(
                exchange='',
                routing_key=QUEUE_NAME,
                body=message,
                properties=pika.BasicProperties(delivery_mode=2)
            )
            print(f" [x] Sent to RabbitMQ: {message}")
        except Exception as e:
            print(f"Failed to send message to RabbitMQ: {e}")
        finally:
            if connection:
                connection.close()

    def _send_to_pubsub(self, message):
        try:
            publisher = pubsub_v1.PublisherClient()
            topic_path = publisher.topic_path(PROJECT_ID, QUEUE_NAME)

            # Ensure the message is in JSON format if necessary
            if not isinstance(message, dict):
                # Convert to dict if it's a plain string
                message = {"message": message}

            json_str = json.dumps(message)
            data = json_str.encode("utf-8")
            future = publisher.publish(topic_path, data=data)
            future.result()  # Wait for the publish to complete
            print(f"Published message to Pub/Sub: {message}")
        except Exception as e:
            print(f"Failed to publish message to Pub/Sub: {e}")
