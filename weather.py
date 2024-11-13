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
        logger.info(f"Starting Weather API")

    def get_weather_data(self):
        try:
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

    def collect_data(self, time_sleep: int = 10, times: int = 1):
        for _ in range(times):
            weather_data = self.get_weather_data()
            time_collected = weather_data["current"]["time"]
            temperature = weather_data["current"]["temperature_2m"]
            self.data["Time"] = time_collected
            self.data["Temperature (celsius)"] = temperature
            time.sleep(time_sleep)
        return self.data

if __name__ == "__main__":
    weather_data = WeatherData(latitude=51.5, longitude=-0.11)
    _ = weather_data.collect_data(time_sleep=1, times=1)
    with open(Path(weather_data.file), "w") as f:
        json.dump(weather_data.model_dump(), f, indent=4)
