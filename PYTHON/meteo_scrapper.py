# weather_plot_open_meteo.py
# Pour lancer : python weather_plot_open_meteo.py
# Nécessite : pip install requests matplotlib

import requests
import matplotlib.pyplot as plt
from datetime import datetime
import sys

def fetch_weather(lat, lon, hours=24):
    """
    Récupère les données météo via Open‑Meteo pour les prochaines heures.
    """
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
    """
    Affiche le graphique des températures horaires.
    """
    times = data["hourly"]["time"]
    temps = data["hourly"]["temperature_2m"]
    # Conversion des temps ISO => datetime
    dates = [datetime.fromisoformat(t) for t in times]

    plt.figure(figsize=(10,5))
    plt.plot(dates, temps, marker="o", linestyle="-", color="orange")
    plt.title("Température horaire")
    plt.xlabel("Date / Heure")
    plt.ylabel("Température (°C)")
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def main():
    # Exemple : Paris (lat, lon)
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
