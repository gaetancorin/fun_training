import requests
from io import BytesIO
from PIL import Image, ImageTk
import tkinter as tk

frames = []  # frames du GIF actuel
anim_id = None  # identifiant de l'after pour annuler l'animation

def animate(counter=0):
    global anim_id
    frame = frames[counter % len(frames)]
    label_img.config(image=frame)
    label_img.image = frame
    anim_id = root.after(100, animate, counter+1)

def get_yesno():
    global frames, anim_id

    # stoppe l'animation en cours
    if anim_id:
        root.after_cancel(anim_id)
        anim_id = None

    try:
        response = requests.get("https://yesno.wtf/api")
        data = response.json()
        answer = data["answer"].capitalize()
        img_url = data["image"]

        img_resp = requests.get(img_url)
        img = Image.open(BytesIO(img_resp.content))

        frames = []
        try:
            while True:
                frame = img.copy().resize((300, 300))
                frames.append(ImageTk.PhotoImage(frame))
                img.seek(len(frames))
        except EOFError:
            pass

        label_text.config(text=f"Réponse : {answer}")
        animate()  # relance l'animation
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
