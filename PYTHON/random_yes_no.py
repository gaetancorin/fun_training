import requests
from io import BytesIO
from PIL import Image, ImageTk
import tkinter as tk


def get_yesno():
    try:
        response = requests.get("https://yesno.wtf/api")
        data = response.json()
        answer = data["answer"].capitalize()
        img_url = data["image"]
        img_resp = requests.get(img_url)
        img = Image.open(BytesIO(img_resp.content))
        img = img.resize((300, 300))  # redimensionne le GIF pour l'affichage
        img_tk = ImageTk.PhotoImage(img)

        label_text.config(text=f"Réponse : {answer}")
        label_img.config(image=img_tk)
        label_img.image = img_tk
    except Exception as e:
        label_text.config(text=f"Erreur : {e}")


root = tk.Tk()
root.title("Yes/No API 🎲")
root.geometry("350x400")

btn = tk.Button(root, text="Tirer une réponse", command=get_yesno)
btn.pack(pady=10)

label_text = tk.Label(root, text="", font=("Arial", 16))
label_text.pack(pady=10)

label_img = tk.Label(root)
label_img.pack()

root.mainloop()