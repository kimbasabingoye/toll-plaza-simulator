import logging
import time
from typing import List, Callable
import random

from vehicle import VehicleType, PlateNumber, Vehicle
from booth_manager import BoothManager

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TollPlazaManager:
    """Manage the entire toll plaza and distribute vehicles to booths."""

    def __init__(self, plaza_id: int, booths: List[BoothManager]):
        self.plaza_id = plaza_id
        self.booths: List[BoothManager] = booths
        self.running = False

    def start_plaza(self):
        """Start all booths in the toll plaza."""
        if not self.running:
            logger.info("Starting toll plaza with %d booths.",
                        len(self.booths))
            for booth in self.booths:
                booth.start_booth()  # Start processing for each booth
            self.running = True
        else:
            logger.info("Toll plaza is already running.")

    def stop_plaza(self):
        """Stop all booths in the toll plaza."""
        if self.running:
            logger.info("Stopping toll plaza.")
            for booth in self.booths:
                booth.stop_booth()  # Stop processing for each booth
            self.running = False
        else:
            logger.info("Toll plaza is not running.")

    def shortest_queue_booth_strategy(self) -> BoothManager:
        """Find the booth with the shortest queue."""
        return min(self.booths, key=lambda booth: booth.booth.vehicle_queue.qsize())

    def random_booth_strategy(self) -> BoothManager:
        """Select a random booth from the list."""
        return random.choice(self.booths)

    def add_vehicle(self, vehicle: Vehicle, strategy: Callable):
        """Add a vehicle to the booth using the given strategy."""
        best_booth = strategy()  # Use the passed strategy function
        if best_booth.add_vehicle(vehicle):
            logger.info("Assigned vehicle %s to booth %d.",
                        vehicle.plate_number, best_booth.booth.booth_id)
        else:
            logger.warning("Failed to assign vehicle %s to booth %d. Booth is full or closed.",
                           vehicle.plate_number, best_booth.booth.booth_id)

    def monitor_booths(self):
        """Monitor the status of each booth."""
        for booth_manager in self.booths:
            if booth_manager.booth.is_processing():
                logger.info(
                    "Booth %d in Toll Plaza %d is currently processing a vehicle.",
                    booth_manager.booth.booth_id, self.plaza_id)
            else:
                logger.info("Booth %d in Toll Plaza %d is available.",
                            booth_manager.booth.booth_id, self.plaza_id)



