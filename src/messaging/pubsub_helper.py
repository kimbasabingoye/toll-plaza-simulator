import json
import logging
from google.cloud import pubsub_v1
from typing import Dict, Any

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PubSubHelper:
    """Helper class for interacting with Google Cloud Pub/Sub."""

    def __init__(self, project_id: str, topic_name: str):
        """Initializes the PubSubHelper with the specified project ID and topic name.

        Args:
            project_id (str): The Google Cloud project ID.
            topic_name (str): The name of the Pub/Sub topic.
        """
        self.publisher = pubsub_v1.PublisherClient()
        self.topic_path = self.publisher.topic_path(project_id, topic_name)

    def publish_message(self, message: Dict[str, Any]) -> None:
        """Publishes a message to the Pub/Sub topic.

        Args:
            message (Dict[str, Any]): The message to publish, represented as a dictionary.

        Raises:
            Exception: If there is an error publishing the message.
        """
        try:
            json_str = json.dumps(message)
            data = json_str.encode("utf-8")
            future = self.publisher.publish(self.topic_path,
                                            data=data)
            #timestamp=message['timestamp'])
            future.result()  # Wait for the publish call to complete.
            logger.info("Published message: %s", message)
        except Exception as e:
            logger.error("Failed to publish message: %s", e)
            raise
