import logging
import random
from typing import List, Optional

from traffic_management.vehicle import Vehicle
from toll_plaza_management.toll_plaza import TollPlaza

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TollPlazasController:
    """Central system to manage multiple toll plazas."""

    def __init__(self, plazas: List[TollPlaza]):
        """
        Initialize the TollPlazasController.

        Args:
            plazas (List[TollPlaza]): List of toll plazas managed by the system.
        """
        self.plazas: List[TollPlaza] = plazas
        self.system_running = False

    def add_plaza(self, toll_plaza: TollPlaza, start_immediately: bool = False):
        """Add a toll plaza to the system."""
        if not any(plaza.plaza_id == toll_plaza.plaza_id for plaza in self.plazas):
            self.plazas.append(toll_plaza)
            logger.info("Toll Plaza %d added to the system.",
                        toll_plaza.plaza_id)
            if start_immediately:
                toll_plaza.start_plaza()
        else:
            logger.info("Toll Plaza %d already exists.", toll_plaza.plaza_id)

    def start_plaza_by_id(self, plaza_id: int):
        """Start the thread for the specified toll plaza."""
        plaza = self._get_plaza_by_id(plaza_id)
        if plaza:
            plaza.start_plaza()
        else:
            logger.error("Toll Plaza %d does not exist.", plaza_id)

    def stop_plaza_by_id(self, plaza_id: int):
        """Stop the thread for the specified toll plaza."""
        plaza = self._get_plaza_by_id(plaza_id)
        if plaza:
            plaza.stop_plaza()
        else:
            logger.error("Toll Plaza %d does not exist.", plaza_id)

    def _get_plaza_by_id(self, plaza_id: int) -> Optional[TollPlaza]:
        """Helper method to retrieve a plaza by its ID."""
        return next((plaza for plaza in self.plazas if plaza.plaza_id == plaza_id), None)

    def start_controller(self):
        """Start the entire toll system by starting all plazas."""
        if not self.system_running:
            logger.info(
                "Starting the central toll system with %d plazas.", len(self.plazas))
            for plaza in self.plazas:
                plaza.start_plaza()
            self.system_running = True
        else:
            logger.info("Central toll system is already running.")

    def stop_controller(self):
        """Stop the entire toll system by stopping all plazas."""
        if self.system_running:
            logger.info("Stopping the central toll system.")
            for plaza in self.plazas:
                plaza.stop_plaza()
            self.system_running = False
        else:
            logger.info("Central toll system is not running.")

    def assign_vehicle_to_plaza(self, new_vehicle: Vehicle):
        """Assign a vehicle to a plaza based on a random selection."""
        selected_plaza = self.find_random_plaza()
        if selected_plaza:
            logger.info("Assigning vehicle %s to plaza %d.",
                        new_vehicle.plate_number, selected_plaza.plaza_id)
            selected_plaza.add_vehicle(
                new_vehicle, selected_plaza.shortest_queue_booth_strategy)
        else:
            logger.error("No plazas available to assign vehicle %s.",
                         new_vehicle.plate_number)

    def find_random_plaza(self) -> Optional[TollPlaza]:
        """Find a random toll plaza, returns None if no plazas are available."""
        return random.choice(self.plazas) if self.plazas else None

    def monitor_system(self):
        """Monitor the status of all plazas."""
        logger.info("Monitoring all plazas.")
        for plaza in self.plazas:
            if plaza.thread and not plaza.thread.is_alive():
                logger.error(
                    "Plaza %d thread is not running. Restarting it.", plaza.plaza_id)
                plaza.start_plaza()
            else:
                plaza.monitor_booths()
