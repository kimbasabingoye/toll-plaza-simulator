import os
import logging
from dotenv import load_dotenv

from traffic_management.booth import Booth
from traffic_management.traffic_generator import TrafficGenerator
from toll_plaza_management.toll_plaza import TollPlaza
from toll_plaza_management.toll_plazas_controller import TollPlazasController
from messaging import message_sender


load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)



def main():
    num_vehicles = int(os.getenv("NUM_VEHICLE", '0'))

    booth11 = Booth("1-1", 
                    message_publisher_type=message_sender.MessagingSystem.PUBSUB)
    booth12 = Booth("1-2",
                    message_publisher_type=message_sender.MessagingSystem.PUBSUB)
    plaza1 = TollPlaza(plaza_id=1, booths=[booth11, booth12])

    booth21 = Booth("2-1")
    booth22 = Booth("2-2")
    plaza2 = TollPlaza(plaza_id=2, booths=[booth21, booth22])

    plazas_controller = TollPlazasController([plaza1, plaza2])

    traffic_generator = TrafficGenerator(plazas_controller, num_vehicles)
    traffic_generator = TrafficGenerator(plazas_controller, 0)

    try:
        traffic_generator.generate_vehicle_flow()
    except KeyboardInterrupt:
        logger.info("Vehicle generation interrupted. Exiting...")
        plazas_controller.stop_controller()  # Gracefully stop all plazas


if __name__ == "__main__":
    main()
