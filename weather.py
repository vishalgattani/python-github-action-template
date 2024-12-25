import json
import time
from collections import defaultdict
from pathlib import Path
from pydantic import BaseModel, Field, HttpUrl
import requests
from logger import logger

class WeatherData(BaseModel):
    latitude: float = Field(default_factory=float, description="Latitude of the location",exclude=False)
    longitude: float = Field(default_factory=float, description="Longitude of the location",exclude=False)
    data: dict = Field(default=defaultdict(list), description="Collected data",exclude=False)
    file:str = Field(default="weather_data.json", description="File to store data",exclude=True)
    url: HttpUrl = Field(default="https://api.open-meteo.com/v1/forecast", description="URL of the API",exclude=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        logger.debug(f"Starting Weather API")

    def get_weather_data(self,latitude: float = None, longitude: float = None):
        try:
            if latitude is None:
                latitude = self.latitude
            if longitude is None:
                longitude = self.longitude
            assert isinstance(latitude, float), "Latitude must be a float"
            assert isinstance(longitude, float), "Longitude must be a float"
            assert self.latitude is not None, "Latitude must be set"
            assert self.longitude is not None, "Longitude must be set"
            response = requests.get(
                self.url,
                params={
                    "latitude": self.latitude,
                    "longitude": self.longitude,
                    "current": "temperature_2m",
                },
            )
            if not response.ok:
                raise Exception(f"{response.reason}: {response.text}")
            return response.json()
        except Exception as e:
            logger.error(e)
            return {}

    def collect_data(self, latitude: float = None, longitude: float = None, time_sleep: float = 0, times: int = 1):
        for _ in range(times):
            try:
                weather_data = self.get_weather_data(latitude=latitude, longitude=longitude)
                if weather_data:
                    time_collected = weather_data["current"]["time"]
                    temperature = weather_data["current"]["temperature_2m"]
                    self.data["Time"].append(time_collected)
                    self.data["Temperature (celsius)"].append(temperature)
                    time.sleep(time_sleep) if time_sleep > 0 else None
            except Exception as e:
                logger.error(e)
        return self.data

if __name__ == "__main__":
    weather_data = WeatherData(latitude=51.5, longitude=-0.11)
    _ = weather_data.collect_data(time_sleep=1, times=1)
    with open(Path(weather_data.file), "w") as f:
        json.dump(weather_data.model_dump(), f, indent=4)
