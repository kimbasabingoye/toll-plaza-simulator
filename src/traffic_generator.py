""" Generate vehicle continously to simulate traffic """

import random
import time
from typing import Optional

from vehicle import VehicleFactory
from rabbitmq_helper import RabbitMQHelper

class TrafficGenerator:
    """
    Class to generate vehicles and send them to the TollPlazaManager.
    """

    def __init__(self, num_vehicles: int,
                 publisher: Optional[RabbitMQHelper] = None):
        """
        Initializes the traffic generator with the number of vehicles and 
        a queue to send vehicles to the toll plaza manager.

        Args:
            num_vehicles (int): The total number of vehicles to generate.
            vehicle_queue (Queue): A queue to hold generated vehicles for the toll plaza manager.
        """
        self.num_vehicles = num_vehicles
        self.client = publisher

    def generate_vehicle_flow(self):
        """
        Continuously generates vehicles and sends them to the toll plaza manager.
        """
        for _ in range(self.num_vehicles):
            # Generate a random vehicle
            vehicle = VehicleFactory.generate_random_vehicle()
            # Logging the generated vehicle
            print(f"{vehicle.to_dict()}")

            # Send the vehicle to the toll plaza manager via the queue
            if self.client:
                self.client.publish_message(vehicle.to_dict())

            # Simulate time between vehicle arrivals
            # Random delay between vehicle generations
            time.sleep(random.uniform(0.5, 1.5))
