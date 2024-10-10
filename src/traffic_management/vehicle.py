"""Vehcile class"""
import os
from enum import Enum
import re
import random

import pydantic

DEFAULT_PLATE_NUMBER_REGEX = r"^[A-Z]{2} \d{4}$"
PLATE_NUMBER_REGEX = os.getenv("PLATE_NUMBER_REGEX", DEFAULT_PLATE_NUMBER_REGEX)

class VehicleType(str, Enum):
    """Class representing the different type of vehicles"""
    CAR = "car"
    TRUCK = "truck"
    VAN = "van"


class PlateNumber(pydantic.BaseModel):
    """Class representing a vehicle plate number"""
    plate_number: str

    @pydantic.field_validator('plate_number')
    @classmethod
    def check_plate_number(cls, input_plate_number) -> str:
        """Check the validity of a plate number against the provided regex pattern."""
        if not re.match(PLATE_NUMBER_REGEX, input_plate_number):
            raise ValueError(f"Invalid plate number: {input_plate_number}")
        return input_plate_number

    def __str__(self):
        return self.plate_number

class Vehicle(pydantic.BaseModel):
    """
    Class representing a vehicle that enters the toll plaza system.
    """
    plate_number: PlateNumber
    vehicle_type: VehicleType

    def __repr__(self):
        """
        Returns a string representation of the vehicle.
        """
        return (f"Plate Number: {self.plate_number}, "
                f"Vehicle Type: {self.vehicle_type},")

    def to_dict(self):
        """Dictionary representation of a vehicle"""
        return {
            'pate_number': f"{self.plate_number}",
            'vehicle_type': self.vehicle_type.value
        }



class VehicleFactory:
    """Class to create Vehicle"""
    @staticmethod
    def _create_vehicle(plate_number_str: str,
                       vehicle_type: VehicleType) -> Vehicle:
        """
        Factory method to create a Vehicle instance.

        Args:
            plate_number_str (str): The license plate number as a string.
            vehicle_type (VehicleType): The type of the vehicle.

        Returns:
            Vehicle: An instance of the Vehicle class.
        """
        plate_number = PlateNumber(plate_number=plate_number_str)
        return Vehicle(plate_number=plate_number,
                       vehicle_type=vehicle_type,
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
        return VehicleFactory._create_vehicle(plate_number_str, vehicle_type)
