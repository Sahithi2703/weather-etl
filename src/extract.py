import requests
from datetime import date, timedelta

URL = "https://api.open-meteo.com/v1/forecast"

CITIES = {
    "Hyderabad": (17.38, 78.48),
    "Bengaluru": (12.97, 77.59),
    "Mumbai": (19.07, 72.88),
}


def extract_city(lat, lon, day):
    """Download one day of hourly weather for one location."""
    params = {
        "latitude": lat,
        "longitude": lon,
        "start_date": day,
        "end_date": day,
        "hourly": "temperature_2m,relative_humidity_2m,precipitation",
        "timezone": "Asia/Kolkata",
    }
    response = requests.get(URL, params=params, timeout=30)
    response.raise_for_status()  # raises an error on 4xx/5xx
    return response.json()


def flatten(city, payload):
    """Turn the API's parallel lists into one dict per hour."""
    hourly = payload["hourly"]
    return [
        {"city": city, "ts": t, "temp_c": temp, "humidity": hum, "precip_mm": rain}
        for t, temp, hum, rain in zip(
            hourly["time"],
            hourly["temperature_2m"],
            hourly["relative_humidity_2m"],
            hourly["precipitation"],
        )
    ]


def extract_all(day):
    """Extract every city for one day."""
    rows = []
    for city, (lat, lon) in CITIES.items():
        payload = extract_city(lat, lon, day)
        rows.extend(flatten(city, payload))
    return rows


if __name__ == "__main__":
    yesterday = (date.today() - timedelta(days=1)).isoformat()
    rows = extract_all(yesterday)
    print(f"Extracted {len(rows)} rows for {yesterday}")
    print(rows[0])