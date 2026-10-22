import requests


def get_coordinates(city_name):
    """Return the latitude, longitude and elevation of a city."""
    url = (
        "https://geocoding-api.open-meteo.com/v1/search?"
        f"name={city_name}&count=1&language=en&format=json"
    )

    response = requests.get(url, timeout=15)
    response.raise_for_status()
    data = response.json()

    if not data.get("results"):
        raise Exception("City not found.")

    city = data["results"][0]
    latitude = city["latitude"]
    longitude = city["longitude"]
    elevation = city.get("elevation", 0)

    return latitude, longitude, elevation


def get_weather_forecast(city_name):
    """Return dates, daily maximum temperatures and minimum temperatures."""
    days = []
    temp_max = []
    temp_min = []

    try:
        latitude, longitude, elevation = get_coordinates(city_name)
    except Exception as error:
        print(f"Could not find city: {error}")
        return days, temp_max, temp_min

    url = "https://api.open-meteo.com/v1/forecast?"
    url += "current_weather=true"
    url += f"&latitude={latitude:.2f}"
    url += f"&longitude={longitude:.2f}"
    url += f"&elevation={elevation:.2f}"

    # Request the 7-day daily forecast and Berlin time zone.
    url += "&daily=temperature_2m_max,temperature_2m_min"
    url += "&timezone=Europe%2FBerlin"
    url += "&forecast_days=7"

    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        data = response.json()

        days = data["daily"]["time"]
        temp_max = data["daily"]["temperature_2m_max"]
        temp_min = data["daily"]["temperature_2m_min"]

    except (requests.RequestException, KeyError, TypeError) as error:
        print(f"Could not retrieve the weather forecast: {error}")

    return days, temp_max, temp_min


if __name__ == "__main__":
    city_name = input("Please enter the name of a city (or 'exit' to quit): ")

    while city_name.lower() != "exit":
        days, temp_max, temp_min = get_weather_forecast(city_name)

        if days:
            print(f"\n7-day weather forecast for {city_name}")
            print("-" * 45)

            for i in range(len(days)):
                print(
                    f"{days[i]}: "
                    f"Maximum: {temp_max[i]} °C, "
                    f"Minimum: {temp_min[i]} °C"
                )

        city_name = input(
            "\nPlease enter another city (or 'exit' to quit): "
        )

    print("Weather forecast app closed.")