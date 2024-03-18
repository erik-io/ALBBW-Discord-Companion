"""
pip install python-dotenv
pip install discord.py
pip install PyMuPDF
"""

import os
from dotenv import load_dotenv
import discord

from check_mail import check_mail

# Load environment variables from .env file
load_dotenv()
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

# Intents are a functionality of Discord that allows specifying what type of events the bot can receive.
# After recent changes in the Discord API, these are explicitly required
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
intents.guilds = True

# Create an instance 'Client' that represents our connection to Discord
client = discord.Client(intents=intents)


@client.event
async def on_ready():
    """
    Event listener that is called when the bot successfully connects to Discord.
    It signals that the bot is ready to receive and process commands.
    """
    print(f"Wir sind eingeloggt als {client.user}")

    # Create a counter to track how many guilds/servers the bot is connected to.
    server_count = 0

    # Loop through all servers the bot is connected to
    for guild in client.guilds:
        # Output the ID and name of the server
        print(f"{guild.name} (Name: {guild.id})")

        # Increase the counter
        server_count += 1

    if server_count > 1:
        print("Der SpeiseplanBot läuft auf " + str(server_count) + " Servern.")
    else:
        print("Der SpeiseplanBot läuft auf " + str(server_count) + " Server.")

    # Send a welcome message to a specific channel
    channel = client.get_channel(1200385984337027124)
    if channel:
        await channel.send("Hallo, ich bin online!")


@client.event
async def on_message(message):
    """
    The event function 'on_message' responds to every message received on the Discord server the bot has access to.
    Initially, every message along with details about the author and the channel is logged in the console.
    If the message exactly matches "essen", the bot responds in the same channel.
    """
    print(f"Log: [{message.channel}] {message.author}: {message.content}")

    if message.content == "essen":
        # Pfad zur .png-Datei, die Sie senden möchten
        file_path = "vorschau.png"
        if os.path.exists(file_path):
            # Erstellen Sie ein discord. File-Objekt mit dem Pfad zur Datei
            file = discord.File(file_path)
            # Senden Sie die Datei im selben Kanal
            await message.channel.send("Hier ist die Vorschau:", file=file)
        else:
            await message.channel.send("Es scheint, als gäbe es keine Vorschau zum Senden.")


if __name__ == "__main__":
    # Check for new emails
    check_mail()
    # Run the bot
    client.run(DISCORD_TOKEN)
