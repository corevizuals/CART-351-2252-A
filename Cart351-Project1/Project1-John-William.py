# ---------------------------------------------
# Project I: Creative Coding in the Terminal
# Title: Breathe Easy - The Air Quality Explorer
# Students: John Compuesto + William Nguyen-Luu
# Professor: Sabine
# Date: Oct 8, 2025
# ---------------------------------------------

import requests
from rich.console import Console
from rich.table import Table
from rich import box
from pyfiglet import Figlet # type: ignore
import time

# ---------------------------------------------
# GLOBAL VARIABLES
# ---------------------------------------------
TOKEN = "6e40e99cd28a98b8a5783356d6d2a3a2cc0810e0"
BASE_SEARCH_URL = "https://api.waqi.info/search/"
BASE_FEED_URL = "https://api.waqi.info/feed/@"
console = Console()

# ---------------------------------------------
# UTILITY FUNCTIONS
# ---------------------------------------------
def get_city_stations(city_name):
    """Fetch all air quality stations for a given city"""
    response = requests.get(BASE_SEARCH_URL, params={"token": TOKEN, "keyword": city_name})
    data = response.json()
    if data["status"] != "ok" or not data["data"]:
        return None
    return data["data"]

def get_station_details(uid):
    """Fetch detailed air quality data for a specific station UID"""
    response = requests.get(f"{BASE_FEED_URL}{uid}/", params={"token": TOKEN})
    data = response.json()
    if data["status"] != "ok":
        return None
    return data["data"]

def classify_aqi(aqi):
    """Return an emoji and color based on AQI level"""
    if aqi is None:
        return ("⚪", "white", "No data")
    aqi = int(aqi)
    if aqi <= 50:
        return ("🌤️", "green", "Good")
    elif aqi <= 100:
        return ("🌥️", "yellow", "Moderate")
    elif aqi <= 150:
        return ("🌫️", "orange", "Unhealthy for Sensitive Groups")
    elif aqi <= 200:
        return ("😷", "red", "Unhealthy")
    elif aqi <= 300:
        return ("☠️", "magenta", "Very Unhealthy")
    else:
        return ("💀", "bright_black", "Hazardous")

# ---------------------------------------------
# MAIN INTERACTIVE LOOP
# ---------------------------------------------
def main():
    console.clear()
    f = Figlet(font="slant")
    console.print(f.renderText("Breathe Easy"), style="bold cyan")
    console.print("Welcome to the Air Quality Explorer 🌍", style="bold white")
    console.print("Type a city name to discover its air quality.\n", style="dim")

    while True:
        city = console.input("[bold cyan]Enter a city (or type 'exit' to quit): [/]")
        if city.lower() == "exit":
            console.print("\nThank you for exploring! Stay safe and breathe easy 🌱\n", style="bold green")
            break

        stations = get_city_stations(city)
        if not stations:
            console.print(f"\n😔 Sorry, no data found for '{city}'. Try another city.\n", style="red")
            continue

        console.print(f"\nFound {len(stations)} station(s) in {city.title()}:\n", style="bold yellow")

        table = Table(title=f"Air Quality in {city.title()}", box=box.SIMPLE_HEAVY)
        table.add_column("Station", style="cyan")
        table.add_column("AQI", justify="center")
        table.add_column("Status", style="bold")
        table.add_column("Dominant Pollutant", style="dim")

        
        for i, s in enumerate(stations, start=1):
            uid = s["uid"]
            station_name = s["station"]["name"]
            console.print(f"Fetching data from station {i}/{len(stations)}: {station_name}...", style="dim")

            try:
                details = requests.get(f"{BASE_FEED_URL}{uid}/", params={"token": TOKEN}, timeout=5).json()
                if details["status"] != "ok":
                    console.print(f"[red]Skipping {station_name} (invalid response)[/red]")
                    continue

                data = details["data"]
                aqi = data["aqi"]
                dom = data.get("dominentpol", "N/A")
                emoji, color, status = classify_aqi(aqi)
                table.add_row(station_name, f"[{color}]{aqi}[/{color}]", f"{emoji} {status}", dom)

            except Exception as e:
                console.print(f"[red]Error fetching {station_name}: {e}[/red]")
                continue

            time.sleep(0.2)

        console.print(table)
        console.print("\n--------------------------------------------\n")

# ---------------------------------------------
# RUN PROGRAM
# ---------------------------------------------
if __name__ == "__main__":
    main()
