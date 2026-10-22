""""
Weather forecast homework
Uses Open-Meteo to show current weather for a city.
Install the requests library first with:
    python -m pip install requests
"""

import requests

 
WEATHER_CODES = {
    0: "Clear sky",
    1: "Mainly clear",
    2: "Partly cloudy",
    3: "Overcast",
    45: "Fog",
    48: "Depositing rime fog",
    51: "Light drizzle",
    53: "Moderate drizzle",
    55: "Dense drizzle",
    56: "Light freezing drizzle",
    57: "Dense freezing drizzle",
    61: "Slight rain",
    63: "Moderate rain",
    65: "Heavy rain",
    66: "Light freezing rain",
    67: "Heavy freezing rain",
    71: "Slight snow fall",
    73: "Moderate snow fall",
    75: "Heavy snow fall",
    77: "Snow grains",
    80: "Slight rain shower",
    81: "Moderate rain shower",
    82: "Violent rain shower",
    85: "Slight snow shower",
    86: "Heavy snow shower",
    95: "Thunderstorm",
    96: "Thunderstorm with slight hail",
    99: "Thunderstorm with heavy hail",
}



def get_coordinates(city_name):
    """Return latitude, longitude, and elevation for a city."""
    url = "https://geocoding-api.open-meteo.com/v1/search"
    params = {
        "name": city_name,
        "count": 3,
        "language": "en",
        "format": "json",
    }

    response = requests.get(url, params=params, timeout=15)
    response.raise_for_status()
    data = response.json()

    if not data.get("results"):
        raise ValueError("City not found. Please check the spelling and try again.")

    result = data["results"][0]
    latitude = result["latitude"]
    longitude = result["longitude"]
    elevation = result.get("elevation", 0)
    return latitude, longitude, elevation


def get_weather(city_name):
    """Return the current weather description and temperature for a city."""
    try:
        latitude, longitude, elevation = get_coordinates(city_name)
    except (requests.RequestException, ValueError, KeyError) as error:
        print(f"Could not find weather for {city_name}: {error}")
        return "Error", float("nan")

    # Build the Open-Meteo weather API request.
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "elevation": elevation,
        "current_weather": "true",
    }

    try:
        response = requests.get(url, params=params, timeout=15)
        response.raise_for_status()
        data = response.json()

        current_weather = data["current_weather"]
        temperature = float(current_weather["temperature"])
        weather_code = int(current_weather["weathercode"])
        weather = WEATHER_CODES.get(weather_code, "Unknown weather")
        return weather, temperature

    except (requests.RequestException, KeyError, TypeError, ValueError) as error:
        print(f"Could not retrieve weather data: {error}")
        return "Error", float("nan")


if __name__ == "__main__":
    while True:
        city = input("Please enter the name of a city (or type 'exit' to quit): ").strip()

        if city.lower() == "exit":
            print("Goodbye!")
            break

        if not city:
            print("Please enter a city name.")
            continue

        weather, temperature = get_weather(city)

        if weather != "Error":
            print(
                f"The current weather in {city} is {weather} "
                f"and the temperature is {temperature:.1f}°C."
            )
