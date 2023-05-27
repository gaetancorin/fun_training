# electricity_consumption_scrapper.py
# Nécessite : pip install pandas matplotlib requests

import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import matplotlib.dates as mdates

def fetch_eco2mix_data():
    """
    Télécharge les données Eco2mix en open data (consommation et production électrique France).
    """
    url = "https://opendata.reseaux-energies.fr/explore/dataset/eco2mix-national-tr/download/?format=csv&timezone=Europe/Paris"
    try:
        df = pd.read_csv(
            url,
            sep=';',
            usecols=[
                'date_heure','consommation','nucleaire','eolien','solaire','hydraulique','fioul','gaz'
            ],
            parse_dates=['date_heure']
        )

        # Nettoyage
        df.rename(columns={'date_heure': 'datetime'}, inplace=True)
        df['datetime'] = pd.to_datetime(df['datetime'], errors='coerce').dt.tz_localize(None)

        # Agrégation par heure (pour éviter les doublons 15min / 30min)
        df = df.groupby('datetime', as_index=False).mean(numeric_only=True)

        return df.dropna(subset=['datetime'])
    except Exception as e:
        print("Erreur lors de la récupération :", e)
        return None

def plot_consumption_and_production(df, hours=48):
    """
    Affiche la consommation et les principales sources de production.
    """
    now = datetime.now()
    df_recent = df[df['datetime'] >= now - timedelta(hours=hours)]

    plt.figure(figsize=(12,6))
    plt.plot(df_recent['datetime'], df_recent['consommation'], label="Consommation", color='black', linewidth=2)

    plt.plot(df_recent['datetime'], df_recent['nucleaire'], label="Nucléaire", color='blue')
    plt.plot(df_recent['datetime'], df_recent['eolien'], label="Éolien", color='green')
    plt.plot(df_recent['datetime'], df_recent['solaire'], label="Solaire", color='orange')
    plt.plot(df_recent['datetime'], df_recent['hydraulique'], label="Hydraulique", color='cyan')
    plt.plot(df_recent['datetime'], df_recent['fioul'], label="Fioul", color='red')
    plt.plot(df_recent['datetime'], df_recent['gaz'], label="Gaz", color='brown')

    plt.title(f"Consommation et production électrique en France (dernières {hours} heures)")
    plt.xlabel("Date / Heure (heure locale)")
    plt.ylabel("Puissance (MW)")
    plt.legend()
    plt.grid(True)
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d/%m %Hh'))
    plt.gca().xaxis.set_major_locator(mdates.AutoDateLocator())
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def main():
    print("Récupération des données Eco2mix…")
    df = fetch_eco2mix_data()
    if df is not None and not df.empty:
        plot_consumption_and_production(df, hours=48)

if __name__ == "__main__":
    main()
