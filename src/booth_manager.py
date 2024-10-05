import time
from vehicle import VehicleType, PlateNumber, Vehicle
from booth import Booth, BoothState
from thread_manager import ThreadManager
import threading
import logging
from typing import Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class BoothManager:
    def __init__(self, booth_id: int, processing_speed: int = 1):
        """
        Initialize the BoothManager with an internal Booth instance.
        
        Args:
            booth_id (int): The unique identifier for the booth.
            processing_speed (float): The speed at which the booth processes vehicles.
        """
        self.booth = Booth(booth_id, processing_speed)
        self.thread = None
        self.running = False

    def start_booth(self):
        """Start the booth's processing in a separate thread."""
        if not self.running:
            self.booth.set_booth_state(BoothState.RUNNING)
            self.thread = threading.Thread(target=self.booth.process_vehicles)
            self.running = True
            self.thread.start()
            logger.info("Booth %d started processing.", self.booth.booth_id)
        else:
            logger.info("Booth %d is already running.", self.booth.booth_id)

    def stop_booth(self):
        """Stop the booth's processing and terminate the thread."""
        if self.running:
            self.booth.set_booth_state(BoothState.STOPPED)
            self.thread.join()  # Wait for the thread to finish
            self.running = False
            logger.info("Booth %d has stopped processing.",
                        self.booth.booth_id)
        else:
            logger.info("Booth %d is not running.", self.booth.booth_id)

    def pause_booth(self):
        """Pause the booth's processing."""
        if self.running:
            self.booth.set_booth_state(BoothState.PAUSED)
            logger.info("Booth %d is paused.", self.booth.booth_id)

    def resume_booth(self):
        """Resume the booth's processing after being paused."""
        if self.booth.is_paused():
            self.booth.set_booth_state(BoothState.RUNNING)
            logger.info("Booth %d has resumed processing.",
                        self.booth.booth_id)

    def open_queue(self):
        """Open the booth's queue to accept new vehicles."""
        self.booth.open_queue()

    def close_queue(self):
        """Close the booth's queue to stop accepting new vehicles."""
        self.booth.close_queue()

    def add_vehicle(self, vehicle: Vehicle):
        """Add a vehicle to the booth's queue."""
        if not self.booth.add_vehicle(vehicle):
            logger.info("Booth %d could not add vehicle %s.",
                        self.booth.booth_id, vehicle.plate_number)


booth = BoothManager(booth_id=1, processing_speed=2)

booth.start_booth()

v1 = Vehicle(plate_number=PlateNumber("AA 1234"), vehicle_type=VehicleType.CAR)
v2 = Vehicle(plate_number=PlateNumber("AA 1235"), vehicle_type=VehicleType.TRUCK)

booth.add_vehicle(v1)
booth.add_vehicle(v2)

time.sleep(10)
booth.stop_booth()
