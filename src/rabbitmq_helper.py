import pika
import json

class RabbitMQHelper():
    def __init__(self, host: str ='localhost',
                 queue_name: str = "", exchange: str ='',
                 routing_key: str = '', durable: bool = True):
        """
        Initialize the RabbitMQ connection and channel.
        
        :param host: RabbitMQ host (default is 'localhost').
        :param queue_name: The queue name to send/receive messages.
        :param exchange: The exchange to bind the queue to (default is '').
        :param routing_key: The routing key used for binding (default is '').
        :param durable: Whether the queue should be durable.
        """
        self.host = host
        self.queue_name = queue_name
        self.exchange = exchange
        self.routing_key = routing_key
        self.durable = durable

        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(self.host)
        )
        self.channel = self.connection.channel()

        if self.queue_name:
            self.channel.queue_declare(
                queue=self.queue_name,
                durable=self.durable
            )

    def publish_message(self, message):
        """
        Publish a message to a queue or exchange.
        
        :param message: The message to publish (should be serializable as JSON).
        """
        self.channel.basic_publish(
            exchange=self.exchange,
            routing_key=self.routing_key or self.queue_name,
            body=json.dumps(message),
            properties=pika.BasicProperties(delivery_mode=2)
        )
        print(f" [X] Sent {message}")

    def consume_message(self, callback):
        """
        Start consuming messages from the queue.
        
        :param callback: A function to process the received messages.
        """
        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(
            queue=self.queue_name,
            on_message_callback=callback,
            auto_ack=False)
        print(
            f" [*] Waiting for messages in {self.queue_name}. To exit press CTRL+C")
        self.channel.start_consuming()

    def close_connection(self):
        """
        Close the connection and channel to RabbitMQ.
        """
        self.channel.close()
        self.connection.close()

    def ack_message(self, delivery_tag):
        """
        Acknowledge a message after processing it.
        
        :param delivery_tag: The delivery tag of the message being acknowledged.
        """
        self.channel.basic_ack(delivery_tag)

    def nack_message(self, delivery_tag, requeue=False):
        """
        Negative acknowledge a message and optionally requeue it.
        
        :param delivery_tag: The delivery tag of the message being nacked.
        :param requeue: Whether to requeue the message (default is False).
        """
        self.channel.basic_nack(delivery_tag, requeue=requeue)
