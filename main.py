import os
from dotenv import load_dotenv
import discord
import imaplib
import email
from email.header import decode_header
import datetime
import fitz

# File to keep track of processed emails
processed_mails = "processed_mails.txt"

# Lädt die Umgebungsvariablen aus der .env-Datei, damit sie im weiteren Code verwendet werden können.
load_dotenv()
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
PASSWORD = os.getenv('PASSWORD')

# Intents sind eine Funktionalität von Discord, die es ermöglicht, anzugeben, welche Art von Ereignissen der Bot
# erhalten kann. Nach neueren Änderungen in der Discord-API sind diese explizit erforderlich.
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
intents.guilds = True

# Wir erstellen eine Instant 'Client', die unsere Verbindung zui Discord repräsentiert
client = discord.Client(intents=intents)

# 'on_ready' ist ein Even-Listener, der aufgerufen wird, wenn der Bot erfolgreich mit Discord verbunden ist.
# Es signalisiert, dass der Bot bereit ist, die Befehle zu empfangen und zu verarbeiten.
@client.event
async def on_ready():
    print(f"Wir sind eingeloggt als {client.user}")

    # Erstellt einen Zähler, um zu verfolgen, mit wie vielen Gilden/Servern der Bot verbunden ist.
    server_count = 0

    # Durchläuft alle Server, mit denen der Bot verbunden ist
    for guild in client.guilds:
        # Ausgabe der ID und Namen des Servers
        print(f"{guild.name} (Name: {guild.id})")

        # Erhöht den Zähler
        server_count += 1

    if server_count > 1:
        print("Der SpeiseplanBot läuft auf " + str(server_count) + " Servern.")
    else:
        print("Der SpeiseplanBot läuft auf " + str(server_count) + " Server.")

    # Sendet eine Willkommensnachricht an einen bestimmten Kanal
    channel = client.get_channel(1200385984337027124)
    if channel:
        await channel.send("Hallo, ich bin online!")


# Die Event-Funktion 'on_message' reagiert auf jede Nachricht, die im Discord-Server empfangen wird, auf den der Bot
# Zugriff hat. Zunächst wird jede Nachricht zusammen mit Details über den Autor und den Kanal in der Konsole
# protokolliert. Wenn die Nachricht genau "test" entspricht, antwortet der Bot im selben Kanal.
@client.event
async def on_message(message):
    print(f"Log: [{message.channel}] {message.author}: {message.content}")

    if message.content == "essen":
        # Pfad zur .png-Datei, die Sie senden möchten
        file_path = "vorschau.png"
        if os.path.exists(file_path):
            # Erstellen Sie ein discord.File-Objekt mit dem Pfad zur Datei
            file = discord.File(file_path)
            # Senden Sie die Datei im selben Kanal
            await message.channel.send("Hier ist die Vorschau:", file=file)
        else:
            await message.channel.send("Es scheint, als gäbe es keine Vorschau zum Senden.")


def check_mail():
    """
    This function checks the email account for new emails with a specific subject line.
    If a new email is found, it downloads any attached PDF files, generates a preview image of the first page, and then deletes the PDF.
    It also marks the email as processed to avoid processing it again in the future.
    """
    # Email account details
    EMAIL = 'weiterleitung@mainsys.tech'
    SERVER = 'imap.hostinger.com'

    # Connect to the email server
    mail = imaplib.IMAP4_SSL(SERVER)
    try:
        # Login to the email account
        mail.login(EMAIL, PASSWORD)
        # Select the inbox
        mail.select('inbox')

        # Get the current week number
        current_kw = datetime.date.today().isocalendar()[1] + 1
        # Check if the email has already been processed
        if mail_already_processed(f"Fwd: Speisenplan KW {current_kw}"):
            print("E-Mail bereits verarbeitet, überspringe...")
            return

        # Search for new emails with the specific subject line
        typ, data = mail.search(None, f'SUBJECT "Fwd: Speisenplan KW {current_kw}"')
        for num in data[0].split():
            # Fetch the email
            typ, data = mail.fetch(num, '(RFC822)')
            # Parse the email
            msg = email.message_from_bytes(data[0][1])
            # Get the subject line
            subject = decode_header(msg["Subject"])[0][0]

            print(f"Neue E-Mail gefunden: {subject}")

            # Loop through the parts of the email
            for part in msg.walk():
                # Skip if the part is multipart or doesn't have a Content-Disposition header
                if part.get_content_maintype() == 'multipart' or part.get('Content-Disposition') is None:
                    continue

                # Get the filename of the part
                filename = part.get_filename()
                # If the part is a PDF file
                if filename and filename.endswith('.pdf'):
                    # Save the PDF file
                    filepath = os.path.join('C:/Users/Mainsys/PycharmProjects/EmailFetch', filename)
                    with open(filepath, 'wb') as f:
                        f.write(part.get_payload(decode=True))
                    print(f"PDF gespeichert: {filepath}")

                    # Generate a preview image of the first page of the PDF
                    doc = fitz.open(filepath)
                    page = doc.load_page(0)
                    pix = page.get_pixmap()
                    output = "vorschau.png"
                    pix.save(output)
                    print(f"PDF-Vorschau gespeichert als {output}")
                    doc.close()
                    # Delete the PDF file
                    os.remove(filepath)
                    # Mark the email as processed
                    mark_mail_as_processed(subject)
    finally:
        print("Keine weiteren E-Mails gefunden, beende Verbindung...")
        # Close the connection to the email server
        mail.close()
        mail.logout()

def mail_already_processed(subject):
    """
    This function checks if an email with the given subject line has already been processed.
    It returns True if the email has been processed, and False otherwise.
    """
    # If the file doesn't exist, the email hasn't been processed
    if not os.path.exists(processed_mails):
        return False
    # Open the file and read the processed emails
    with open(processed_mails, "r") as file:
        mail_processed = file.read().splitlines()
    # Check if the email is in the list of processed emails
    return subject in mail_processed

def mark_mail_as_processed(subject):
    """
    This function marks an email with the given subject line as processed.
    It does this by appending the subject line to the file of processed emails.
    """
    # Open the file and append the subject line
    with open(processed_mails, "a") as file:
        file.write(subject + "\n")

if __name__ == "__main__":
    # Check for new emails
    check_mail()
    # Run the bot
    client.run(DISCORD_TOKEN)

