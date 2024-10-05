import time

from toll_plaza_manager import TollPlazaManager
from  booth_manager import BoothManager
from vehicle import Vehicle, PlateNumber, VehicleType, VehicleFactory
from traffic_generator import TrafficGenerator

NUM_VEHICLE = 100

traffic = TrafficGenerator(100)

# Create some Booth instances
booth1 = BoothManager(booth_id=1, processing_speed=2)
booth2 = BoothManager(booth_id=2, processing_speed=3)
booth3 = BoothManager(booth_id=3, processing_speed=1)

# Pass the list of BoothManager instances to the TollPlazaManager
toll_plaza = TollPlazaManager(1, booths=[booth1, booth2, booth3])

# Start the toll plaza
toll_plaza.start_plaza()

for _ in range(NUM_VEHICLE):
    veh = VehicleFactory.generate_random_vehicle()
    toll_plaza.add_vehicle(veh, toll_plaza.random_booth_strategy)
    time.sleep(1)

# Let it run for a while
time.sleep(10)

# Stop the toll plaza
toll_plaza.stop_plaza()
