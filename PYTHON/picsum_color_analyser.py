import requests
from io import BytesIO
from PIL import Image
from collections import Counter
import matplotlib.pyplot as plt

# URL de l'image
url = "https://picsum.photos/200/300"
response = requests.get(url)
img = Image.open(BytesIO(response.content))
img = img.convert("RGB")

# Réduction pour analyse rapide
img_small = img.resize((50, 50))
pixels = list(img_small.getdata())

# Compter les couleurs
color_counts = Counter(pixels)
top_colors = color_counts.most_common(5)

colors = [color for color, count in top_colors]
counts = [count for color, count in top_colors]
hex_colors = ['#%02x%02x%02x' % color for color in colors]

# Affichage
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(6, 8))

# 1. Image originale
ax1.imshow(img)
ax1.axis('off')
ax1.set_title("Image originale")

# 2. Graphique des couleurs dominantes
ax2.bar(range(len(top_colors)), counts, color=hex_colors)
ax2.set_xticks(range(len(top_colors)))
ax2.set_xticklabels(hex_colors)
ax2.set_ylabel("Nombre de pixels")
ax2.set_title("Top 5 couleurs dominantes")

plt.tight_layout()
plt.show()
