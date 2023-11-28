import os
import time
import requests
from io import BytesIO
from PIL import Image
import numpy as np
import colorsys
import pandas as pd

NUM_IMAGES = 20
OUTPUT_DIR = "robots"
SIZE = (256, 256)

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

# === Étape 2 : Extraction des caractéristiques visuelles ===
features = []

for ident, img in zip(ids, images):
    arr = np.array(img) / 255.0
    mask = ~(np.all(arr == [0, 0, 0], axis=-1))
    arr = arr[mask]

    r, g, b = arr.mean(axis=0)
    hsv = np.array([colorsys.rgb_to_hsv(*px) for px in arr])
    h_mean, s_mean, v_mean = hsv.mean(axis=0)

    features.append({
        "id": ident,
        "mean_r": round(r * 255, 1),
        "mean_g": round(g * 255, 1),
        "mean_b": round(b * 255, 1),
        "saturation": round(s_mean, 3),
        "luminosity": round(v_mean, 3)
    })

df = pd.DataFrame(features)
print("\nAperçu des caractéristiques extraites :")
print(df.head())
