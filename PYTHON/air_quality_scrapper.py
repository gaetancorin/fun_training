# air_quality_scrapper.py
# Pour lancer : python air_quality_scrapper.py
# Script pour récupérer et afficher la qualité de l'air (PM10, PM2.5) sur Paris
# en temps réel via Open-Meteo, sans clé API.

import requests
import matplotlib.pyplot as plt
from datetime import datetime
import matplotlib.dates as mdates
import sys

def fetch_air_quality(lat, lon, hours=48):
    url = (
        f"https://air-quality-api.open-meteo.com/v1/air-quality?"
        f"latitude={lat}&longitude={lon}"
        f"&hourly=pm10,pm2_5"
        f"&forecast_hours={hours}"
    )
    resp = requests.get(url)
    if resp.status_code != 200:
        print("Erreur lors de la récupération des données :", resp.status_code, resp.text)
        return None
    return resp.json()

def plot_air_quality(data):
    times = data["hourly"]["time"]
    pm10 = data["hourly"]["pm10"]
    pm25 = data["hourly"]["pm2_5"]

    dates = [datetime.fromisoformat(t) for t in times]

    # Filtrage pour lisibilité (une valeur toutes les 3 heures)
    dates_filtered = dates[::3]
    pm10_filtered = pm10[::3]
    pm25_filtered = pm25[::3]

    plt.figure(figsize=(12,6))
    plt.plot(dates_filtered, pm10_filtered, label="PM10", marker="o")
    plt.plot(dates_filtered, pm25_filtered, label="PM2.5", marker="o")

    plt.title("Air Quality (µg/m³)")
    plt.xlabel("Date / Heure")
    plt.ylabel("Concentration (µg/m³)")
    plt.grid(True)
    plt.legend()

    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d/%m %Hh'))
    plt.gca().xaxis.set_major_locator(mdates.AutoDateLocator())
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def main():
    # Exemple par défaut : Paris (48.8566, 2.3522)
    lat = 48.8566
    lon = 2.3522
    if len(sys.argv) == 3:
        try:
            lat = float(sys.argv[1])
            lon = float(sys.argv[2])
        except ValueError:
            print("Usage : python air_quality_scrapper.py [latitude] [longitude]")
            sys.exit(1)

    print(f"Récupération des données de qualité de l'air pour lat={lat}, lon={lon} …")
    data = fetch_air_quality(lat, lon, hours=48)
    if data:
        plot_air_quality(data)

if __name__ == "__main__":
    main()
