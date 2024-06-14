import smtplib
from dotenv import load_dotenv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

# Load .env file
load_dotenv()
smtp_user = os.getenv("SMTP_USER") # sender email
smtp_pass = os.getenv("SMTP_PASS") # sender password application

smtp_server = os.getenv("SMTP_SERVER") # receiver SMTP server
smtp_port = int(os.getenv("SMTP_PORT")) # receiver SMTP port (587=TLS, 465=SSL, 25=not secure)
receiver = os.getenv("RECEIVER") # receiver email

def send_email():
    sender = smtp_user

    msg = MIMEMultipart("alternative")
    msg["From"] = sender
    msg["To"] = receiver
    msg["Subject"] = "✅ Test SMTP Python"

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

    msg.attach(MIMEText(text, "plain"))
    msg.attach(MIMEText(html, "html"))

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            if smtp_port == 587:
                server.starttls()  # securise TLS
            server.login(smtp_user, smtp_pass)
            server.sendmail(sender, receiver, msg.as_string())
        print("✅ Email envoyé avec succès à", receiver)

    except Exception as e:
        print("❌ Erreur lors de l'envoi :", e)

if __name__ == "__main__":
    send_email()
