
import logging
import threading
from typing import List, Optional

from toll_plaza_management.toll_plaza_business_logic import (
    TollPlazaBusinessLogic,
    TollPlazaState)
from traffic_management.booth import Booth

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TollPlaza(TollPlazaBusinessLogic):
    """Class to encapsulate a toll plaza and its associated thread."""

    def __init__(self, plaza_id: int, booths: List[Booth]):
        """
        Initialize the toll plaza and set up threading.

        Args:
            plaza_id (int): Unique ID for the toll plaza.
            booths (List[BoothManager]): List of BoothManager instances.
        """
        super().__init__(plaza_id, booths)  # Correctly initialize the parent class
        self.thread: Optional[threading.Thread] = None
        self.state: TollPlazaState = TollPlazaState.CLOSED

    def is_closed(self):
        return self.state == TollPlazaState.CLOSED

    def start_plaza(self):
        """Start the plaza, which means starting the thread associated with this toll plaza."""
        if self.is_closed():
            logger.info("Starting Toll Plaza %d.", self.plaza_id)
            self.thread = threading.Thread(
                target=self._start_plaza_logic, name=f"Plaza-{self.plaza_id}")
            self.thread.start()
            self.state = TollPlazaState.OPEN
            logger.info("Toll Plaza %d is now OPEN.", self.plaza_id)
        else:
            logger.info("Toll Plaza %d is already running.", self.plaza_id)

    def stop_plaza(self):
        """Stop the plaza by stopping the thread associated with this toll plaza."""
        if not self.is_closed():
            logger.info("Stopping Toll Plaza %d.", self.plaza_id)
            self._stop_plaza_logic()  # Call the business logic to stop the plaza
            if self.thread:
                self.thread.join()  # Wait for the thread to finish
                logger.info("Stopped thread for Toll Plaza %d.", self.plaza_id)
