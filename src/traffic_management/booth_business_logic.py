import time
import os
import enum
import logging
from datetime import datetime
from queue import Queue
from typing import Dict, Any, Optional

from dotenv import load_dotenv

from traffic_management.vehicle import Vehicle

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BOTH_QUEUE_MAX_SIZE = int(os.getenv("BOTH_QUEUE_MAX_SIZE", "10"))


class AddVehiculeReturnCode(int, enum.Enum):
    """Error codes for adding vehicle"""
    QUEUE_FULL = 1
    QUEUE_CLOSED = 2
    QUEUE_VEHICULE_ADDED = 0


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


class BoothBusinessLogic:
    """Represents a booth in a toll plaza."""

    def __init__(self,
                 booth_id: str,
                 processing_speed: float = 1,
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
        self.queue_state = queue_state

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

    def open_queue_logic(self) -> None:
        """Open the booth and start accepting vehicles."""
        self.set_queue_state(BoothQueueState.OPEN)
        logger.info("Booth %s queue is now open to new vehicles.",
                    self.booth_id)

    def close_queue_logic(self) -> None:
        """Close the booth and stop accepting new vehicles."""
        self.set_queue_state(BoothQueueState.CLOSED)
        logger.info("Booth %s queue is now closed to new vehicles.",
                    self.booth_id)

    def enqueue_vehicle(self, new_vehicle: Vehicle) -> int:
        """
        Adds a vehicle to the processing queue of the booth if it's not full 
        and the booth is open.

        Args:
            new_vehicle (Vehicle): the vehicle to add
        Returns:
            bool: True if the vehicle is added, False otherwise
        """
        if self.queue_state == BoothQueueState.CLOSED:
            logger.info("Booth %s queue is closed. Cannot add vehicle %s.",
                        self.booth_id, new_vehicle.plate_number)
            return AddVehiculeReturnCode.QUEUE_CLOSED

        if self.queue_is_full():
            logger.info("Booth %s: Queue is full. Cannot add vehicle %s.",
                        self.booth_id, new_vehicle.plate_number)
            return AddVehiculeReturnCode.QUEUE_FULL

        self.vehicle_queue.put(new_vehicle)
        return AddVehiculeReturnCode.QUEUE_VEHICULE_ADDED

    def get_event(self, vehicle: Vehicle,
                  booth_event: BoothEventType) -> Dict[str, Any]:
        """ Build and return event dict """
        vehicle_dict = vehicle.to_dict()
        event = {"event_type": booth_event.value,
                 "timestamp": datetime.now().isoformat(),
                 "booth_id": self.booth_id}
        event.update(vehicle_dict)

        return event

    def _set_next_vehicle_to_process(self) -> bool:
        """
        Get the next vehicleto process from the queue and set it as the 
        curent vehicle to process
        """
        if not self.is_busy() and not self.queue_is_empty():
            self.current_vehicle = self.vehicle_queue.get()
            if self.current_vehicle:
                logger.info("Booth %s is now processing the vehicle %s.",
                            self.booth_id,
                            self.current_vehicle.plate_number.plate_number)
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

