import os
import time
import requests
from io import BytesIO
from PIL import Image

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
