from weather import WeatherData
from logger import logger
from pathlib import Path
import json

def main():
    latitude = 51.5
    longitude = -0.11
    weather_data = WeatherData(latitude=latitude, longitude=longitude)
    data = weather_data.collect_data(latitude=latitude, longitude=longitude)
    logger.info(f"Collected data for latitude: {latitude}, longitude: {longitude}: {data.get('Time')[-1]}: {data.get('Temperature (celsius)')[-1]}")
    with open(Path(weather_data.file), "w") as f:
        json.dump(weather_data.model_dump(), f, indent=4)

if __name__ == "__main__":
    main()