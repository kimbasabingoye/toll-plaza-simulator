import os

import pika
import dotenv

dotenv.load_dotenv()

QUEUE_NAME = os.getenv("QUEUE_NAME", "")
RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "")

class MessageConsumer:
    def __init__(self, queue_name: str, rabbitmq_host: str):
        self.queue_name = queue_name
        self.rabbitmq_host = rabbitmq_host

    def consume_message(self, callback):
        """
        Start consuming messages from the queue.

        :param callback: A function to process the received messages.
        """
        # Establish connection to RabbitMQ
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=self.rabbitmq_host))
        channel = connection.channel()

        # Set QoS settings for fair dispatch
        channel.basic_qos(prefetch_count=1)

        # Start consuming messages
        print(f"Using QUEUE_NAME: {self.queue_name}")
        channel.basic_consume(
            queue=self.queue_name,
            on_message_callback=callback,
            auto_ack=False
        )

        print(
            f" [*] Waiting for messages in {self.queue_name}. To exit press CTRL+C")
        try:
            channel.start_consuming()
        except KeyboardInterrupt:
            print(" [*] Stopping consumption...")
        finally:
            connection.close()

# Example callback function to process the received messages


def callback(ch, method, properties, body):
    print(f" [x] Received {body.decode()}")
    # Process the message here (e.g., log it, save it, etc.)
    ch.basic_ack(delivery_tag=method.delivery_tag)  # Acknowledge the message


# Create a consumer instance and start consuming messages
if __name__ == "__main__":
    consumer = MessageConsumer(QUEUE_NAME, RABBITMQ_HOST)
    consumer.consume_message(callback)
