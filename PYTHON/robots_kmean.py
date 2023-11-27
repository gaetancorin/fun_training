import os
import time
import requests
from io import BytesIO
from PIL import Image

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
