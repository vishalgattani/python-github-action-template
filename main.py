from weather import WeatherData
from logger import logger
from pathlib import Path
import json

def main():
    weather_data = WeatherData(latitude=51.5, longitude=-0.11)
    _ = weather_data.collect_data(time_sleep=1, times=1)
    logger.debug(f"Collected data: {weather_data.model_dump_json()}")
    with open(Path(weather_data.file), "w") as f:
        json.dump(weather_data.model_dump(), f, indent=4)

if __name__ == "__main__":
    main()