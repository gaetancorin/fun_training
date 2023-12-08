import os
import time
import requests
from io import BytesIO
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

NUM_IMAGES = 20
OUTPUT_DIR = "faces"
SIZE = (256, 256)

os.makedirs(OUTPUT_DIR, exist_ok=True)

images = []
ids = []

print(f"Téléchargement de {NUM_IMAGES} visages dans ./{OUTPUT_DIR}/ ...")

for i in range(1, NUM_IMAGES + 1):
    ident = f"face_{i}"
    ids.append(ident)
    url = "https://thispersondoesnotexist.com"
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        img = Image.open(BytesIO(resp.content)).convert("RGB")
        img = img.resize(SIZE)
        images.append(img)
        filename = os.path.join(OUTPUT_DIR, f"{ident}.png")
        img.save(filename)
        print(f"[{i}/{NUM_IMAGES}] sauvegardé -> {filename}")
    except Exception as e:
        print(f"[{i}/{NUM_IMAGES}] erreur pour {ident}: {e}")
    time.sleep(0.2)

print(f"\nTerminé : {len(images)} visages téléchargés et sauvegardés dans '{OUTPUT_DIR}'.")

# --- Étape 2 : comparer tous les visages ---
arrs = [np.array(img) for img in images]
min_diff = float("inf")
closest_pair = (0, 1)

for i in range(NUM_IMAGES):
    for j in range(i + 1, NUM_IMAGES):
        diff = np.mean(np.abs(arrs[i] - arrs[j]))
        if diff < min_diff:
            min_diff = diff
            closest_pair = (i, j)

i1, i2 = closest_pair
print(f"\nLes deux visages les plus proches sont : {ids[i1]} et {ids[i2]} (diff moyenne = {min_diff:.2f})")

# --- Étape 3 : afficher les deux visages les plus proches ---
plt.figure(figsize=(8, 4))
plt.subplot(1, 2, 1)
plt.imshow(images[i1])
plt.axis('off')
plt.title(ids[i1])

plt.subplot(1, 2, 2)
plt.imshow(images[i2])
plt.axis('off')
plt.title(ids[i2])

plt.tight_layout()
plt.show()
