import os
import time
import requests
from io import BytesIO
from PIL import Image
import numpy as np
import colorsys
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

NUM_IMAGES = 20
OUTPUT_DIR = "robots"
SIZE = (256, 256)
NUM_CLUSTERS = 7

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/141.0.0.0 Safari/537.36"
}

os.makedirs(OUTPUT_DIR, exist_ok=True)

images = []
ids = []

print(f"Téléchargement de {NUM_IMAGES} robots dans ./{OUTPUT_DIR}/ ...")

for i in range(1, NUM_IMAGES + 1):
    ident = f"robot_{i}"
    ids.append(ident)
    url = f"https://robohash.org/{ident}.png?size={SIZE[0]}x{SIZE[1]}"
    try:
        resp = requests.get(url, headers=headers, timeout=10)
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

print(f"\nTerminé : {len(images)} images téléchargées et sauvegardées dans '{OUTPUT_DIR}'.")

# Étape 2 : extraction des caractéristiques visuelles
features = []

for ident, img in zip(ids, images):
    arr = np.array(img) / 255.0
    mask = ~(np.all(arr == [0, 0, 0], axis=-1))
    arr = arr[mask]
    r, g, b = arr.mean(axis=0)
    hsv = np.array([colorsys.rgb_to_hsv(*px) for px in arr])
    h_mean, s_mean, v_mean = hsv.mean(axis=0)
    features.append([r, g, b, s_mean, v_mean])

X = np.array(features)

# Étape 3 : clustering KMeans
kmeans = KMeans(n_clusters=NUM_CLUSTERS, random_state=42)
labels = kmeans.fit_predict(X)

# Organisation des robots par cluster
clustered = {i: [] for i in range(NUM_CLUSTERS)}
for label, img, ident in zip(labels, images, ids):
    clustered[label].append((ident, img))

# Affichage amélioré
rows = NUM_CLUSTERS
cols = max(len(items) for items in clustered.values())
plt.figure(figsize=(cols * 2, rows * 2.5))

for cluster_idx, items in clustered.items():
    for i, (ident, img) in enumerate(items):
        plt.subplot(rows, cols, cluster_idx * cols + i + 1)
        plt.imshow(img)
        plt.axis('off')
        if i == 0:
            plt.ylabel(f"Cluster {cluster_idx}", fontsize=12, rotation=0, labelpad=40)

plt.tight_layout()
plt.show()
