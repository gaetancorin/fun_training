import requests
from io import BytesIO
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

# Compare deux robots RoboHash en ignorant strictement les pixels noirs (0,0,0)
def get_robot_image(text):
    url = f"https://robohash.org/{text}.png"
    response = requests.get(url)
    if response.status_code == 200:
        return Image.open(BytesIO(response.content)).convert("RGB")
    else:
        raise Exception(f"Erreur de téléchargement pour {text}")

def compare_images(img1, img2):
    img1 = img1.resize((256, 256))
    img2 = img2.resize((256, 256))

    arr1 = np.array(img1)
    arr2 = np.array(img2)

    # Masque : pixels NON noirs dans les deux images
    mask1 = np.any(arr1 != [0, 0, 0], axis=-1)
    mask2 = np.any(arr2 != [0, 0, 0], axis=-1)
    mask = np.logical_and(mask1, mask2)

    # Appliquer le masque (on ne garde que les pixels non noirs dans les 2 images)
    arr1_masked = arr1[mask]
    arr2_masked = arr2[mask]

    # Éviter les différences de taille après masquage
    n = min(len(arr1_masked), len(arr2_masked))
    arr1_masked = arr1_masked[:n]
    arr2_masked = arr2_masked[:n]

    diff = np.abs(arr1_masked - arr2_masked)
    mean_diff = diff.mean()
    similarity = 100 - (mean_diff / 255) * 100
    return similarity

if __name__ == "__main__":
    word1 = input("Premier mot : ").strip()
    word2 = input("Deuxième mot : ").strip()

    img1 = get_robot_image(word1)
    img2 = get_robot_image(word2)

    similarity = compare_images(img1, img2)

    plt.figure(figsize=(8, 4))
    plt.subplot(1, 2, 1)
    plt.imshow(img1)
    plt.title(f"Robot: {word1}")
    plt.axis("off")

    plt.subplot(1, 2, 2)
    plt.imshow(img2)
    plt.title(f"Robot: {word2}")
    plt.axis("off")

    plt.suptitle(f"Similarité (sans pixels 0,0,0) : {similarity:.2f} %", fontsize=14)
    plt.tight_layout()
    plt.show()
