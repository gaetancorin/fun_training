import os
import time
import requests
from PIL import Image
from io import BytesIO
import numpy as np
import colorsys
import matplotlib.pyplot as plt

NUM_IMAGES = 15
SIZE = 500
OUTPUT_DIR = "picsum_images_square"

os.makedirs(OUTPUT_DIR, exist_ok=True)

images = []
dominant_colors = []
image_names = []

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
        image_names.append(f"image_{i}.png")

        arr = np.array(img) / 255.0
        mask = ~(np.all(arr == [0, 0, 0], axis=-1))
        arr = arr[mask]
        mean_rgb = arr.mean(axis=0)
        dominant_colors.append(mean_rgb)

        print(f"[{i}/{NUM_IMAGES}] sauvegardé -> {filename} | couleur dominante: {mean_rgb}")
    except Exception as e:
        print(f"[{i}/{NUM_IMAGES}] erreur :", e)
    time.sleep(0.2)

# --- Tri des images par teinte HSV ---
hsv_colors = [colorsys.rgb_to_hsv(*rgb) for rgb in dominant_colors]
sorted_indices = np.argsort([h for h, s, v in hsv_colors])
sorted_images = [images[i] for i in sorted_indices]
sorted_names = [image_names[i] for i in sorted_indices]

# --- Affichage en arc-en-ciel ---
plt.figure(figsize=(20, 6))
for idx, img in enumerate(sorted_images):
    plt.subplot(1, NUM_IMAGES, idx + 1)
    plt.imshow(img)
    plt.axis('off')
plt.suptitle("Arc-en-ciel de 15 images Picsum triées par couleur dominante")
plt.tight_layout()
plt.show()
