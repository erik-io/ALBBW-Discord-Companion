"""
pip install python-dotenv
pip install discord.py
pip install PyMuPDF
"""
import datetime
import os
from dotenv import load_dotenv
import discord
import logging

# from Vegans import vegan_food
from check_mail import check_mail

# Set the logging level to INFO
logging.basicConfig(filename='bot.log', level=logging.INFO, format = '%(asctime)s - %(levelname)s - %(message)s')

# Create a console handler with level INFO
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# Create a formatter and add it to the handler
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)

# Add the handler to the root logger
logging.getLogger('').addHandler(console_handler)

# Load environment variables from .env file
try:
    logging.info("Loading environment variables from .env file")
    load_dotenv()
    DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

    # Check if the Discord token is set
    if DISCORD_TOKEN is None:
        raise ValueError("DISCORD_TOKEN is not set")
    else:
        logging.info("DISCORD_TOKEN is set")
except ValueError as e:
    logging.error(e) # Log the error message
    exit(1) # Exit the program with a status code of 1

logging.info("Environment variables loaded successfully")

# Get the current week number
current_kw = datetime.date.today().isocalendar()[1]

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
    admin_role = discord.utils.get(channel.guild.roles, name="Admin")
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

    message_to_lower = message.content.lower()

    if message_to_lower == "essen":
        # Pfad zur .png-Datei, die Sie senden möchten
        file_path = f"vorschau_{current_kw}.png"
        if os.path.exists(file_path):
            # Erstellen Sie ein discord. File-Objekt mit dem Pfad zur Datei
            file = discord.File(file_path)
            await message.channel.send("Hier ist die Vorschau:", file=file)
        else:
            await message.channel.send("Es scheint, als gäbe es keine Vorschau zum Senden.")


async def ping_role(role_name, message):
    """
    This function sends a message to a specific channel and pings a specific role.
    """
    channel = client.get_channel(1200385984337027124)
    role = discord.utils.get(channel.guild.roles, name=role_name)
    if channel:
        # Send a message and ping the role
        await channel.send(f"<@&{role.id}> {message}")

if __name__ == "__main__":
    # Run the bot
    try:
        client.run(DISCORD_TOKEN)
    except discord.LoginFailure:
        logging.error("Invalid or expired DISCORD_TOKEN")
        exit(1)  # Exit the program with a status code of 1

    # Check for new emails
    check_mail()