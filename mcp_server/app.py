import httpx
from mcp.server import FastMCP

app = FastMCP("Weather Assistant Server", port=9300)


async def get_lat_lon(place_name: str):
    """
    Return (latitude, longitude) for a given place_name using
    OSM Nominatim’s public JSON API—no API key needed.
    """
    try:
        url = "https://nominatim.openstreetmap.org/search"
        params = {
            "q": place_name,       # free-form query string
            "format": "json",      # request JSON output
            "limit": 1             # top result only
        }
        headers = {
            "User-Agent": "dummy-geocoder/1.0 (+https://example.org/)"  
            # custom UA required by policy :contentReference[oaicite:3]{index=3}
        }

        async with httpx.AsyncClient() as client:
            resp = await client.get(url, params=params, headers=headers)

        resp.raise_for_status()         # HTTP errors → exceptions
        results = resp.json()           # parse JSON array

        if not results:
            raise ValueError(f"No results for '{place_name}'")

        # Extract and return floats
        lat = float(results[0]["lat"])
        lon = float(results[0]["lon"])
        return lat, lon
    except Exception as e:
        print(f"Error in get_lat_lon: {e}")
        return None, None


@app.tool()
async def get_weather_info(place_name: str) -> dict:
    """
    Get weather information for a specific location. Returns info for the next 7 days
    Also returns today's date
    Args:
        place_name: Name of the place
    Returns:
        A dict with weather predictions for the next 7 days and today's date
    """
    try:
        lat, lon = await get_lat_lon(place_name)
        if not lat or not lon:
            print("Latitide and Longitude not found")
            return {"error": "Latitide and Longitude not found"}

        url = "https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": lat,
            "longitude": lon,
            "daily": ["temperature_2m_max", "temperature_2m_min", "precipitation_probability_max"],
            "timezone": "auto"
        }

        async with httpx.AsyncClient() as client:
            resp = await client.get(url, params=params)

        resp.raise_for_status()
        data = resp.json()

        today_date = data["daily"]["time"][0]
        weather_preds = {day: {} for day in data["daily"]["time"]}
        for i, time in enumerate(data["daily"]["time"]):
            weather_preds[time]["max_temp"] = data["daily"]["temperature_2m_max"][i]
            weather_preds[time]["min_temp"] = data["daily"]["temperature_2m_min"][i]
            weather_preds[time]["precipitation_probability"] = data["daily"]["precipitation_probability_max"][i]

        return {
            "today_date": today_date,
            "weather_preds": weather_preds
        }
    except Exception as e:
        print(f"Error in get_weather_info: {e}")
        return {"error": "Error getting the weather information"}


if __name__ == "__main__":
    app.run(transport="sse")
