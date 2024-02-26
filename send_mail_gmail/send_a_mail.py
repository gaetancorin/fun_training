import smtplib
from dotenv import load_dotenv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
receiver = os.getenv("RECEIVER")

load_dotenv()
smtp_user = os.getenv("SMTP_USER")
smtp_pass = os.getenv("SMTP_PASS")

smtp_server = os.getenv("SMTP_SERVER")
smtp_port = int(os.getenv("SMTP_PORT"))


def send_email():
    sender = smtp_user

    # Création du message
    msg = MIMEMultipart("alternative")
    msg["From"] = sender
    msg["To"] = receiver
    msg["Subject"] = "✅ Test SMTP Python"

    # Contenu du mail
    text = "Bonjour Gaetan,\n\nCeci est un test SMTP envoyé en Python."
    html = """\
    <html>
      <body>
        <p>Bonjour Gaetan,<br><br>
           Ceci est un <b>test SMTP</b> envoyé en Python. 🚀<br>
        </p>
      </body>
    </html>
    """

    # Attache texte + html
    msg.attach(MIMEText(text, "plain"))
    msg.attach(MIMEText(html, "html"))

    try:
        # Connexion au serveur SMTP
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.login(smtp_user, smtp_pass)
            server.sendmail(sender, receiver, msg.as_string())
        print("✅ Email envoyé avec succès à", receiver)

    except Exception as e:
        print("❌ Erreur lors de l'envoi :", e)

if __name__ == "__main__":
    send_email()
