import os
from dotenv import load_dotenv
import discord

# Lädt die Umgebungsvariablen aus der .env-Datei, damit sie im weiteren Code verwendet werden können.
load_dotenv()
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

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

    if message.content == "test":
        await message.channel.send("Es funktioniert!")

client.run(DISCORD_TOKEN)