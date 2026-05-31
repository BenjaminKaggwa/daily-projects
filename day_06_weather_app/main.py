import requests

def get_coordinates(city):
    url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1"
    data = requests.get(url).json()
    if not data.get("results"):
        return None, None, None
    r = data["results"][0]
    return r["latitude"], r["longitude"], r["name"]

def get_weather(lat, lon):
    url = (f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}"
           f"&current_weather=true&hourly=relativehumidity_2m&timezone=auto")
    return requests.get(url).json()

def weather_description(code):
    codes = {0:"Clear sky",1:"Mainly clear",2:"Partly cloudy",3:"Overcast",
             45:"Foggy",48:"Icy fog",51:"Light drizzle",53:"Drizzle",61:"Light rain",
             63:"Rain",65:"Heavy rain",71:"Light snow",73:"Snow",80:"Rain showers",
             95:"Thunderstorm"}
    return codes.get(code, "Unknown")

def main():
    print("=== Weather App ===")
    while True:
        city = input("\nEnter city (or 'quit'): ").strip()
        if city.lower() == "quit":
            break
        lat, lon, name = get_coordinates(city)
        if not lat:
            print("City not found. Try again.")
            continue
        data = get_weather(lat, lon)
        w = data["current_weather"]
        humidity = data["hourly"]["relativehumidity_2m"][0]
        print(f"\n📍 {name}")
        print(f"🌡  Temperature : {w['temperature']}°C")
        print(f"💨 Wind speed  : {w['windspeed']} km/h")
        print(f"💧 Humidity    : {humidity}%")
        print(f"🌤  Condition   : {weather_description(w['weathercode'])}")

if __name__ == "__main__":
    main()
