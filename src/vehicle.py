"""Vehcile class"""

from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime
import re
import random
from typing import Optional, Dict, Any


class VehicleType(str, Enum):
    """Class representing the different type of vehicles"""
    CAR = "car"
    TRUCK = "truck"
    VAN = "van"


class PlateNumber:
    """Class representing a vehicle plate number"""

    def __init__(self, plate_number: str):
        if not self.is_valid(plate_number):
            raise ValueError(f"Invalid plate number: {plate_number}")
        self.plate_number = plate_number

    @staticmethod
    def is_valid(plate_number: str) -> bool:
        """Check the validity of a plate_number"""
        return bool(re.match(r"^[A-Z]{2} \d{4}$", plate_number))

    def __str__(self):
        return self.plate_number


@dataclass
class Vehicle:
    """
    Class representing a vehicle that enters the toll plaza system.
    """
    plate_number: PlateNumber
    vehicle_type: VehicleType
    #entry_time: str
    #processed_time: Optional[str] = field(init=False, default=None)

    def __repr__(self):
        """
        Returns a string representation of the vehicle.
        """
        return (f"Vehicle(plate_number={self.plate_number}, "
                f"vehicle_type={self.vehicle_type}, "
                #f"entry_time={self.entry_time}, "
                #f"processed_time={self.processed_time})"
                )


    def to_dict(self) -> Dict[str, Any]:
        """
            Returns a dict representation of the vehicle.
            """
        return {
            "plate_number": self.plate_number.plate_number,
            "vehicle_type": self.vehicle_type.value,
            #"entry_time": self.entry_time,
            #"processed_time": self.processed_time
        }


class VehicleFactory:
    """Class to create Vehicle"""
    @staticmethod
    def create_vehicle(plate_number_str: str,
                       vehicle_type: VehicleType) -> Vehicle:
        """
        Factory method to create a Vehicle instance.

        Args:
            plate_number_str (str): The license plate number as a string.
            vehicle_type (VehicleType): The type of the vehicle.

        Returns:
            Vehicle: An instance of the Vehicle class.
        """
        plate_number = PlateNumber(plate_number_str)
        #entry_time = datetime.now().isoformat()
        return Vehicle(plate_number=plate_number,
                       vehicle_type=vehicle_type,
                       #entry_time=entry_time
                    )

    @staticmethod
    def generate_random_vehicle() -> Vehicle:
        """
        Generate a vehicle with random attributes.

        Returns:
            Vehicle: An instance of the Vehicle class with random attributes.
        """
        plate_letters = random.choice(['AA', 'AB', 'CD', 'CF', 'GA'])
        plate_numbers = random.randint(1000, 9999)
        plate_number_str = f"{plate_letters} {plate_numbers}"
        vehicle_type = random.choice(list(VehicleType))
        return VehicleFactory.create_vehicle(plate_number_str, vehicle_type)
