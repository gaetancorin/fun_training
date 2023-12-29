import os
import time
import requests
from PIL import Image
from io import BytesIO
import numpy as np
import colorsys

NUM_IMAGES = 30
SIZE = 500  # image carrée 500x500
OUTPUT_DIR = "picsum_images_square"

os.makedirs(OUTPUT_DIR, exist_ok=True)

images = []
dominant_colors = []

for i in range(1, NUM_IMAGES + 1):
    url = f"https://picsum.photos/{SIZE}/{SIZE}?random={i}"
    try:
        resp = requests.get(url)
        resp.raise_for_status()
        img = Image.open(BytesIO(resp.content)).convert("RGB")
        w, h = img.size
        min_edge = min(w, h)
        left = (w - min_edge) // 2
        top = (h - min_edge) // 2
        right = left + min_edge
        bottom = top + min_edge
        img = img.crop((left, top, right, bottom))
        img = img.resize((SIZE, SIZE))
        filename = os.path.join(OUTPUT_DIR, f"image_{i}.png")
        img.save(filename)
        images.append(img)

        # --- Extraction couleur dominante ---
        arr = np.array(img) / 255.0
        mask = ~(np.all(arr == [0, 0, 0], axis=-1))  # ignore le noir
        arr = arr[mask]
        mean_rgb = arr.mean(axis=0)
        dominant_colors.append(mean_rgb)

        print(f"[{i}/{NUM_IMAGES}] sauvegardé -> {filename} | couleur dominante: {mean_rgb}")
    except Exception as e:
        print(f"[{i}/{NUM_IMAGES}] erreur :", e)
    time.sleep(0.2)

print(f"\nTerminé : {len(images)} images carrées téléchargées avec couleur dominante extraite.")
