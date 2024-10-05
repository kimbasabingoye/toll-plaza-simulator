import time
import os
import enum
import logging
from datetime import datetime
from queue import Queue
from typing import Dict, Any, Optional

from dotenv import load_dotenv

from vehicle import Vehicle

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BOTH_QUEUE_MAX_SIZE = int(os.getenv("BOTH_QUEUE_MAX_SIZE", "10"))


class BoothEventType(str, enum.Enum):
    """Class representing booth events"""
    ENTER = 'enter'
    PAY = "pay"
    EXIT = "exit"


class BoothState(str, enum.Enum):
    """Class representing booth state"""
    STOPPED = 'stopped'
    PAUSED = 'paused'
    RUNNING = 'running'

class BoothQueueState(str, enum.Enum):
    """Class representing booth's queue state"""
    OPEN = 'open'
    CLOSED = 'closed'


class Booth:
    """Represents a booth in a toll plaza."""

    def __init__(self,
                 booth_id: int,
                 processing_speed: int = 1,
                 state: BoothState = BoothState.RUNNING,
                 queue_length: int = BOTH_QUEUE_MAX_SIZE,
                 queue_state: BoothQueueState = BoothQueueState.OPEN,
                 ):
        """
        Initialize a Booth instance.

        Args:
            booth_id (int): The unique identifier for the booth.
            processing_speed (float): The speed at which the booth processes
            vehicles.
        """
        self.booth_id = booth_id
        self.current_vehicle: Optional[Vehicle] = None
        self.vehicle_queue = Queue(queue_length)
        self.processing_speed = processing_speed
        self.state = state
        self.queue_state = queue_state

    def is_running(self):
        return self.state == BoothState.RUNNING

    def is_paused(self):
        return self.state == BoothState.PAUSED

    def is_stopped(self):
        return self.state == BoothState.STOPPED

    def is_busy(self) -> bool:
        """ Return True if the booth is busy and False if not """
        return self.current_vehicle is not None

    def queue_is_closed(self) -> bool:
        return self.queue_state == BoothQueueState.CLOSED

    def queue_is_open(self) -> bool:
        return self.queue_state == BoothQueueState.OPEN

    def queue_is_full(self) -> bool:
        """ Returns true if the booth queue is full and false otherwise"""
        return self.vehicle_queue.full()

    def queue_is_empty(self) -> bool:
        """ Returns true if the booth queue is empty and false otherwise """
        return self.vehicle_queue.empty()

    def set_queue_state(self, new_state):
        self.queue_state = new_state

    def set_booth_state(self, state):
        self.state = state

    def open_queue(self) -> None:
        """Open the booth and start accepting vehicles."""
        self.set_queue_state(BoothQueueState.OPEN)
        logger.info("Booth %d queue is now open to new vehicles.",
                    self.booth_id)

    def close_queue(self) -> None:
        """Close the booth and stop accepting new vehicles."""
        self.set_queue_state(BoothQueueState.CLOSED)
        logger.info("Booth %d queue is now closed to new vehicles.",
                    self.booth_id)

    def add_vehicle(self, new_vehicle: Vehicle) -> bool:
        """
        Adds a vehicle to the processing queue of the booth if it's not full 
        and the booth is open.

        Args:
            new_vehicle (Vehicle): the vehicle to add
        Returns:
            bool: True if the vehicle is added, False otherwise
        """
        if self.queue_state == BoothQueueState.CLOSED:
            logger.info("Booth %d queue is closed. Cannot add vehicle %d.",
                        self.booth_id, new_vehicle.plate_number)
            return False

        if self.queue_is_full():
            logger.info("Booth %d: Queue is full. Cannot add vehicle %d.",
                        self.booth_id, new_vehicle.plate_number)
            return False

        self.vehicle_queue.put(new_vehicle)
        return True

    def get_event(self, vehicle: Vehicle,
                  booth_event: BoothEventType) -> Dict[str, Any]:
        """ Build and return event dict """
        vehicle_dict = vehicle.to_dict()
        event = {"event_type": booth_event,
                 "timestamp": datetime.now().isoformat()}
        event.update(vehicle_dict)

        return event

    def _set_next_vehicle_to_process(self) -> bool:
        """
        Get the next vehicleto process from the queue and set it as the 
        curent vehicle to process
        """
        if not self.is_busy() and not self.queue_is_empty():
            self.current_vehicle = self.vehicle_queue.get()
            logger.info("Booth %d is now processing the vehicle %s.",
                        self.booth_id, self.current_vehicle.plate_number.plate_number)
            return True
        return False

    def process_current_vehicle(self) -> bool:
        """Simulate processing the curent vehicle."""
        if self.current_vehicle is None:
            logger.info("No vehicle no process")
            return False

        entrance_message = self.get_event(
            self.current_vehicle, BoothEventType.ENTER)
        time.sleep(self.processing_speed / 3)
        logger.info("Publishing entrance event: %s",
                    entrance_message)

        payment_message = self.get_event(
            self.current_vehicle, BoothEventType.PAY)
        time.sleep(self.processing_speed / 3)
        logger.info("Publishing payment event: %s",
                    payment_message)

        exit_message = self.get_event(
            self.current_vehicle, BoothEventType.EXIT)
        time.sleep(self.processing_speed / 3)
        logger.info("Publishing exit event: %s", exit_message)

        self.current_vehicle = None  # Reset current vehicle after processing

        return True

    def process_vehicles(self):
        """Process vehicle continuoulsy"""
        while self.is_running():
            if self.is_paused():
                logger.info(
                    "Booth %d is paused. No processing will occur.",
                    self.booth_id)
                time.sleep(1)  # Wait before checking again
            elif self._set_next_vehicle_to_process():
                self.process_current_vehicle()
                time.sleep(0.5)
            else:
                logger.info(
                    "Booth %d is idle. No vehicles to process.", self.booth_id)
                time.sleep(1)  # Wait before checking again
