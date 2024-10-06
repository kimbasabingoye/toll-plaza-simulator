import threading
import logging
from typing import Optional
import time
import os

from dotenv import load_dotenv

from traffic_management.booth_business_logic import (
    BoothBusinessLogic, BoothState, AddVehiculeReturnCode,
    BoothQueueState)
from traffic_management.vehicle import Vehicle

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

VEHICLE_PROCESSING_SLEEP_TIME = float(os.getenv(
    "VEHICLE_PROCESSING_SLEEP_TIME", "0.5"))

class Booth(BoothBusinessLogic):
    """Class representing booth"""

    def __init__(self, booth_id: str, processing_speed: int = 1):
        super().__init__(booth_id, processing_speed)
        self.thread: Optional[threading.Thread] = None
        self.state: BoothState = BoothState.STOPPED

    def is_running(self):
        """Returns True if the booth is running and False otherwise"""
        return self.state == BoothState.RUNNING

    def is_paused(self):
        """Returns True if the booth is paused and False otherwise"""
        return self.state == BoothState.PAUSED

    def is_stopped(self):
        """Returns True if the booth is sopped and False otherwise"""
        return self.state == BoothState.STOPPED

    def start_booth(self):
        """Start the booth's processing in a separate thread."""
        if not self.is_running():
            self.state = BoothState.RUNNING
            self.thread = threading.Thread(target=self.process_vehicles)
            self.thread.start()
            self.open_queue()
            logger.info("Booth %s started processing.", self.booth_id)
        else:
            logger.info("Booth %s is already running.", self.booth_id)

    def stop_booth(self):
        """Stop the booth's processing and terminate the thread."""
        if self.is_running():
            self.queue_state = BoothQueueState.CLOSED
            # wait until all vehicle in the queue are processed
            start_time = time.time()
            # Timeout after 10 seconds
            while not self.queue_is_empty() and (time.time() - start_time < 10):
                time.sleep(2)
            if self.thread:
                self.thread.join()
                self.state = BoothState.STOPPED
                self.close_queue()
                logger.info("Booth %s has stopped processing.",
                            self.booth_id)
        else:
            logger.info("Booth %s is not running.", self.booth_id)

    def pause_booth(self):
        """Pause the booth's processing."""
        if self.is_running():
            self.state = BoothState.PAUSED
            logger.info("Booth %s is paused.", self.booth_id)
        else:
            logger.info(
                "Booth %s cannot be paused because it is not running.",
                self.booth_id)

    def resume_booth(self):
        """Resume the booth's processing after being paused."""
        if self.is_paused():
            self.state = BoothState.RUNNING
            logger.info("Booth %s has resumed processing.",
                        self.booth_id)

    def open_queue(self):
        """Open the booth's queue to accept new vehicles."""
        self.open_queue_logic()

    def close_queue(self):
        """Close the booth's queue to stop accepting new vehicles."""
        self.close_queue_logic()

    def add_vehicle(self, new_vehicle: Vehicle) -> bool:
        """Add a vehicle to the booth's queue."""
        if self.enqueue_vehicle(new_vehicle) != AddVehiculeReturnCode.QUEUE_VEHICULE_ADDED:
            logger.info("Booth %s could not add vehicle %s.",
                        self.booth_id, new_vehicle.plate_number)
            return False
        return True

    def process_vehicles(self):
        """Process vehicle continuoulsy"""
        while True:
            if self.is_stopped():
                logger.info(
                    "Booth %s queue is closed. Stopping vehicle processing.",
                    self.booth_id)
                break

            if self._set_next_vehicle_to_process():
                self.process_current_vehicle()
                time.sleep(VEHICLE_PROCESSING_SLEEP_TIME)
            else:
                logger.info(
                    "Booth %s is idle. No vehicles to process.", self.booth_id)
                time.sleep(1)  # Wait before checking again



