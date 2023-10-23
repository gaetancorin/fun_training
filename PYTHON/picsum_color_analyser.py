import requests
from io import BytesIO
from PIL import Image
from collections import Counter

# URL de l'image (Picsum pour l'exemple)
url = "https://picsum.photos/200/300"

# Récupérer l'image
response = requests.get(url)
img = Image.open(BytesIO(response.content))

# Convertir en RGB si nécessaire
img = img.convert("RGB")

# Reduire la taille pour accélérer l'analyse
img_small = img.resize((50, 50))

# Extraire toutes les couleurs
pixels = list(img_small.getdata())

# Compter les couleurs
color_counts = Counter(pixels)

# Afficher les 5 couleurs les plus fréquentes
top_colors = color_counts.most_common(5)
print("Top 5 couleurs dominantes (RGB) :")
for color, count in top_colors:
    print(color, ":", count, "pixels")

# Optionnel : afficher l'image
img.show()
