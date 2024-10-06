# Toll Plaza Simulator

## Overview
The Toll Plaza Management System is a simulation project designed to manage multiple toll plazas and assign vehicles to them efficiently. The system uses a central controller to oversee the operations of various toll plazas, each equipped with multiple booths. Vehicles are generated randomly and assigned to the toll plazas based on predefined strategies.

## Features
1. Dynamic Vehicle Generation: Randomly generate vehicles using the VehicleFactory.
2. Multiple Toll Plazas: Manage multiple toll plazas, each with several booths.
3. Centralized Control: A central controller (TollPlazasController) manages the operations of all toll plazas.
4. Simulation Control: Start, monitor, and stop the simulation with ease.
5. Environment Configuration: Configure the number of vehicles to simulate using environment variables.

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/toll-plaza-management.git
   cd toll-plaza-management
   ```
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Set up environment variables: Create a .env file in the root directory of the project and add the following:
   ```text
   NUM_VEHICLE=100  # Set the number of vehicles to simulate
   ```

## Usage
1. Run the simulation
   ```sh
   python main.py
   ```
2. Interrupt the simulation: Press Ctrl+C to stop the simulation.

## Project Structure
```
├── config                    # Configuration files for the project
│   ├── __init__.py          # Package initialization file
│   └── settings.py          # Configuration settings, such as environment variables
├── docs                      # Documentation files related to the project
│   ├── Class Diagram.drawio  # Class diagram for visual representation of project architecture
├── LICENSE                   # License file for the project
├── README.md                 # Project overview and instructions for usage
├── requirements.txt          # List of dependencies required to run the project
├── scripts                   # Directory for auxiliary scripts (if any)
├── src                       # Source code of the project
│   ├── main.py               # Entry point of the application
│   ├── messaging             # Messaging-related modules
│   │   ├── pubsub_helper.py   # Helper functions for publish/subscribe messaging
│   │   └── rabbitmq_helper.py  # Functions for RabbitMQ messaging operations
│   ├── toll_plaza_management  # Modules for managing toll plazas
│   │   ├── __init__.py       # Package initialization file
│   │   ├── toll_plaza_business_logic.py # Business logic for toll plaza operations
│   │   ├── toll_plaza.py     # TollPlaza class representing a toll plaza
│   │   └── toll_plazas_controller.py # Controller for managing multiple toll plazas
│   └── traffic_management     # Modules for managing traffic and vehicles
│       ├── booth_business_logic.py # Business logic for booth operations
│       ├── booth.py          # Booth class representing individual booths
│       ├── traffic_generator.py # Module for generating traffic and assigning vehicles
│       └── vehicle.py        # Vehicle class and factory for creating vehicles
└── tests                     # Unit tests for project components
    ├── test_booth.py        # Tests for the Booth class functionality
    ├── test_toll_plaza.py   # Tests for the TollPlaza class functionality
    └── test_vehicle.py       # Tests for the Vehicle class functionality
```

## Contributing
Contributions are welcome! Please fork the repository and submit a pull request for any improvements or bug fixes.

## License
This project is licensed under the MIT License. See the LICENSE file for details.

## Contact
For any questions or suggestions, please open an issue on GitHub or contact me through linkedin @kimbasabingoye.