from datetime import datetime
from typing import Tuple
import json
from pathlib import Path
from geopy.distance import geodesic
import boto3  # For AWS IoT Core integration

class EnvironmentalMonitor:
    def __init__(self) -> None:
        """Initializes the environmental monitor with default values."""
        self._last_update_time: datetime = datetime.now()
        self._last_longitude: float = None
        self._last_latitude: float = None
        self._send_remote: bool = False
        self._last_particulate_reading: float = None

    @property
    def last_update_time(self) -> datetime:
        """Last update time getter."""
        return self._last_update_time

    @last_update_time.setter
    def last_update_time(self, value: datetime) -> None:
        """Last update time setter."""
        self._last_update_time = value

    @property
    def last_longitude(self) -> float:
        """Last longitude getter."""
        return self._last_longitude

    @last_longitude.setter
    def last_longitude(self, value: float) -> None:
        """Last longitude setter."""
        self._last_longitude = value

    @property
    def last_latitude(self) -> float:
        """Last latitude getter."""
        return self._last_latitude

    @last_latitude.setter
    def last_latitude(self, value: float) -> None:
        """Last latitude setter."""
        self._last_latitude = value

    @property
    def send_remote(self) -> bool:
        """Send remote flag getter."""
        return self._send_remote

    @send_remote.setter
    def send_remote(self, value: bool) -> None:
        """Send remote flag setter."""
        self._send_remote = value

    @property
    def last_particulate_reading(self) -> float:
        """Last particulate reading getter."""
        return self._last_particulate_reading

    @last_particulate_reading.setter
    def last_particulate_reading(self, value: float) -> None:
        """Last particulate reading setter."""
        self._last_particulate_reading = value

    def calculate_distance_moved(self, current_latitude: float, current_longitude: float) -> float:
        """
        Calculates the distance moved in feet between the last and current coordinates.

        Args:
            current_latitude (float): The current latitude.
            current_longitude (float): The current longitude.

        Returns:
            float: The distance moved in feet.
        """
        if self._last_latitude is None or self._last_longitude is None:
            return 0.0
        last_coords = (self._last_latitude, self._last_longitude)
        current_coords = (current_latitude, current_longitude)
        return geodesic(last_coords, current_coords).feet

    def read_gps_coordinates(self) -> Tuple[float, float]:
        """
        Reads the current GPS coordinates from the GPS module.

        Returns:
            Tuple[float, float]: The current latitude and longitude.
        """
        # Placeholder for actual GPS reading code
        current_latitude, current_longitude = 34.0522, -118.2437  # Example coordinates
        self._last_latitude = current_latitude
        self._last_longitude = current_longitude
        return current_latitude, current_longitude

    def read_environmental_data(self) -> float:
        """
        Reads the current environmental data from the sensor.

        Returns:
            float: The current particulate reading.
        """
        # Placeholder for actual environmental data reading code
        particulate_reading = 15.5  # Example particulate reading
        self._last_particulate_reading = particulate_reading
        return particulate_reading

    def save_data_to_json(self, file_path: Path) -> None:
        """
        Saves the current environmental data to a JSON file.

        Args:
            file_path (Path): The path to the file where data should be saved.
        """
        data = {
            "last_update_time": self._last_update_time.isoformat(),
            "last_longitude": self._last_longitude,
            "last_latitude": self._last_latitude,
            "last_particulate_reading": self._last_particulate_reading,
        }
        with open(file_path, 'w') as f:
            json.dump(data, f)

    def send_data_to_aws_iot(self, aws_iot_topic: str) -> None:
        """
        Sends the current environmental data to AWS IoT Core if send_remote is True.

        Args:
            aws_iot_topic (str): The AWS IoT Core topic to publish the data to.
        """
        if not self._send_remote:
            return
        client = boto3.client('iot-data', region_name='us-east-1')
        payload = {
            "state": {
                "reported": {
                    "last_update_time": self._last_update_time.isoformat(),
                    "last_longitude": self._last_longitude,
                    "last_latitude": self._last_latitude,
                    "last_particulate_reading": self._last_particulate_reading,
                }
            }
        }
        client.publish(
            topic=aws_iot_topic,
            qos=1,
            payload=json.dumps(payload)
        )
