import yfinance as yf
import matplotlib.pyplot as plt

btc = yf.Ticker("BTC-USD")
data = btc.history(period="30d", interval="1h")  # 30 jours, intervalle 1h

plt.plot(data.index, data['Close'], label="BTC")
plt.xlabel("Date")
plt.ylabel("Prix (USD)")
plt.title("Historique BTC 30 jours")
plt.legend()
plt.show()
