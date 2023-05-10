# weather_plot_open_meteo.py
# Pour lancer : python weather_plot_open_meteo.py
# Nécessite : pip install requests matplotlib

import requests
import matplotlib.pyplot as plt
from datetime import datetime
import matplotlib.dates as mdates
import sys

def fetch_weather(lat, lon, hours=48):
    url = (
        f"https://api.open-meteo.com/v1/forecast?"
        f"latitude={lat}&longitude={lon}"
        f"&hourly=temperature_2m"
        f"&forecast_hours={hours}"
        f"&temperature_unit=celsius"
    )
    resp = requests.get(url)
    if resp.status_code != 200:
        print("Erreur lors de la récupération des données météo :", resp.status_code, resp.text)
        return None
    return resp.json()

def plot_temperature(data):
    times = data["hourly"]["time"]
    temps = data["hourly"]["temperature_2m"]

    dates = [datetime.fromisoformat(t) for t in times]

    # Filtrer pour ne pas surcharger l'axe X (une valeur toutes les 3 heures)
    dates_filtered = dates[::3]
    temps_filtered = temps[::3]

    plt.figure(figsize=(12,5))
    plt.plot(dates_filtered, temps_filtered, marker="o", linestyle="-", color="orange")
    plt.title("Température horaire")
    plt.xlabel("Date / Heure")
    plt.ylabel("Température (°C)")

    # Formater l'axe X pour afficher jour/mois et heure
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d/%m %Hh'))
    plt.gca().xaxis.set_major_locator(mdates.AutoDateLocator())

    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def main():
    # Exemple : Paris
    lat = 48.8566
    lon = 2.3522
    if len(sys.argv) == 3:
        try:
            lat = float(sys.argv[1])
            lon = float(sys.argv[2])
        except ValueError:
            print("Usage : python weather_plot_open_meteo.py [latitude] [longitude]")
            sys.exit(1)

    print(f"Récupération météo pour lat={lat}, lon={lon} …")
    weather = fetch_weather(lat, lon, hours=48)
    if weather:
        plot_temperature(weather)

if __name__ == "__main__":
    main()
