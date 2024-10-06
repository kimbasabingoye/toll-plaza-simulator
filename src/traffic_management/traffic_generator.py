import time
import logging
import math
import random
from traffic_management.vehicle import VehicleFactory
from toll_plaza_management.toll_plazas_controller import TollPlazasController

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TrafficGenerator:
    """
    Class to generate vehicles and send them to the TollPlazaManager.
    """

    def __init__(self, plazas_controller: TollPlazasController, num_vehicles: int = 0):
        self.central_system = plazas_controller
        self.generated_count = 0
        if num_vehicles != 0:
            self.num_vehicles = num_vehicles
        else:
            self.num_vehicles = math.inf

    def generate_vehicle_flow(self):
        """
        Continuously generates vehicles and sends them to the toll plaza controller.
        """
        logger.info("Starting vehicle generation...")
        self.central_system.start_controller()

        try:
            while self.generated_count < self.num_vehicles:
                veh = VehicleFactory.generate_random_vehicle()
                try:
                    self.central_system.assign_vehicle_to_plaza(veh)
                    logger.info("Vehicle %s assigned to a plaza.",
                                veh.plate_number)
                    self.generated_count += 1
                except Exception as e:
                    logger.error("Failed to assign vehicle %s: %s",
                                 veh.plate_number, str(e))

                if self.generated_count % 10 == 0:  # Monitor every 10 vehicles
                    logger.info("Monitoring system status...")
                    self.central_system.monitor_system()

                time.sleep(random.uniform(0.5, 2.0))
        except KeyboardInterrupt:
            logger.info("Stopping vehicle generation.")
            self.central_system.stop_controller()  # Gracefully stop all plazas
