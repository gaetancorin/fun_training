import requests
from io import BytesIO
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

# Compare deux robots générés par RoboHash en mesurant la différence moyenne de pixels

def get_robot_image(text):
    url = f"https://robohash.org/{text}.png"
    response = requests.get(url)
    if response.status_code == 200:
        return Image.open(BytesIO(response.content)).convert("RGB")
    else:
        raise Exception(f"Erreur lors du téléchargement pour {text}")

def compare_images(img1, img2):
    # Redimensionner les deux images à la même taille
    img1 = img1.resize((256, 256))
    img2 = img2.resize((256, 256))

    arr1 = np.array(img1)
    arr2 = np.array(img2)

    # Calcul de la différence moyenne des pixels (Mean Absolute Error)
    diff = np.abs(arr1 - arr2)
    mean_diff = diff.mean()
    similarity = 100 - (mean_diff / 255) * 100  # score en %
    return similarity

if __name__ == "__main__":
    word1 = input("Premier mot : ").strip()
    word2 = input("Deuxième mot : ").strip()

    img1 = get_robot_image(word1)
    img2 = get_robot_image(word2)

    similarity = compare_images(img1, img2)

    # Affichage
    plt.figure(figsize=(8, 4))
    plt.subplot(1, 2, 1)
    plt.imshow(img1)
    plt.title(f"Robot: {word1}")
    plt.axis("off")

    plt.subplot(1, 2, 2)
    plt.imshow(img2)
    plt.title(f"Robot: {word2}")
    plt.axis("off")

    plt.suptitle(f"Similarité estimée : {similarity:.2f} %", fontsize=14)
    plt.tight_layout()
    plt.show()
