import logging
from typing import List, Callable
import random
import enum

from traffic_management.booth import Booth
from traffic_management.vehicle import Vehicle

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TollPlazaState(str, enum.Enum):
    """Class representing plaza state."""
    OPEN = 'open'
    CLOSED = 'closed'


class NoAvailableBoothsException(Exception):
    """Exception raised when no booths are available."""

    def __init__(self, message="No available booths."):
        self.message = message
        super().__init__(self.message)


class TollPlazaBusinessLogic:
    """Encapsulates the core business logic for managing a toll plaza."""

    def __init__(self, plaza_id: int, booths: List[Booth]):
        self.plaza_id = plaza_id
        self.booths: List[Booth] = booths

    def _start_plaza_logic(self):
        """Start all booths in the toll plaza."""
        logger.info("Starting toll plaza %d with %d booths.",
                    self.plaza_id, len(self.booths))
        for current_booth in self.booths:
            current_booth.start_booth()  # Start processing for each booth
        logger.info("Toll plaza %d started.", self.plaza_id)

    def _stop_plaza_logic(self):
        """Stop the toll plaza by stopping all the booths."""
        logger.info("Stopping Toll Plaza %d.", self.plaza_id)
        for booth in self.booths:
            booth.stop_booth()  # Stop processing for each booth
        # Fixed the log message
        logger.info("Toll plaza %d stopped.", self.plaza_id)

    def shortest_queue_booth_strategy(self) -> Booth:
        """Find the booth with the shortest queue."""
        available_booths = [
            booth for booth in self.booths if booth.queue_is_open()]
        if not available_booths:
            logger.warning("No available booths to process vehicles.")
            raise NoAvailableBoothsException()
        return min(available_booths, key=lambda booth: booth.vehicle_queue.qsize())

    def random_booth_strategy(self) -> Booth:
        """Select a random booth from the list."""
        available_booths = [
            booth for booth in self.booths if booth.queue_is_open()]
        if not available_booths:
            logger.warning("No available booths to process vehicles.")
            raise NoAvailableBoothsException()
        return random.choice(available_booths)

    def add_vehicle(self, vehicle: Vehicle, strategy: Callable[[], Booth]):
        """Add a vehicle to the booth using the given strategy."""
        booth: Booth = strategy()  # Use the passed strategy function
        if booth.add_vehicle(vehicle):
            logger.info("Assigned vehicle %s to booth %s.",
                        vehicle.plate_number, booth.booth_id)
        else:
            logger.warning("Failed to assign vehicle %s to booth %d. Booth is full or closed.",
                           vehicle.plate_number, booth.booth_id)

    def monitor_booths(self):
        """Monitor the status of each booth."""
        for booth in self.booths:
            if booth.is_busy():
                logger.info(
                    "Booth %d in Toll Plaza %d is currently processing a vehicle.",
                    booth.booth_id, self.plaza_id)
            else:
                logger.info("Booth %d in Toll Plaza %d is available.",
                            booth.booth_id, self.plaza_id)
