import os
import datetime
import logging
import configparser
from logging.handlers import RotatingFileHandler
from dotenv import load_dotenv
import discord

# Import custom modules
# from Vegans import vegan_food
from check_mail import check_mail

# Initialize logging
def setup_logging():
    """
    This function sets up the logging for the application. It reads the logging level from a configuration file,
    sets up a rotating file handler for the log file and a console handler for console output. Both handlers use
    the same formatter for their log messages. The function also sets the logging level for the root logger.
    """

    # Create a config parser
    config = configparser.ConfigParser()

    # Read the configuration file
    config.read('config.ini')

    # Get the logging level from the configuration file, defaulting to 'INFO' if not found
    log_level = config.get('LOGGING', 'log_level', fallback='INFO')

    # Create a formatter for the log messages
    log_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    # Create a rotating file handler for the log file
    # The log file will be 'bot.log', with a maximum size of 5MB, and a maximum of 1 backup files
    log_file_handler = RotatingFileHandler('bot.log', maxBytes=5*1024*1024, backupCount=1)

    # Set the formatter for the file handler
    log_file_handler.setFormatter(log_formatter)

    # Set the logging level for the file handler
    log_file_handler.setLevel(getattr(logging, log_level.upper(), logging.INFO))

    # Create a console handler for console output
    console_handler = logging.StreamHandler()

    # Set the logging level for the console handler
    console_handler.setLevel(getattr(logging, log_level.upper(), logging.INFO))

    # Set the formatter for the console handler
    console_handler.setFormatter(log_formatter)

    # Set the logging configuration for the root logger
    # The root logger will have two handlers: the file handler and the console handler
    logging.basicConfig(handlers=[log_file_handler, console_handler], level=logging.DEBUG)

    # Log a message indicating that logging has been set up successfully
    logging.info("Logging set up successfully")

# Call the setup_logging function to set up logging
setup_logging()

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

logging.debug("Environment variables loaded successfully")

# Get the current week number
logging.debug("Getting current date and week number")
current_kw = datetime.date.today().isocalendar()[1]
logging.debug(f"Current week number: {current_kw}")

# Intents are a functionality of Discord that allows specifying what type of events the bot can receive.
# After recent changes in the Discord API, these are explicitly required
logging.debug("Setting up intents")
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
intents.guilds = True
logging.debug("Intents set up successfully")

# Create an instance 'Client' that represents our connection to Discord
client = discord.Client(intents=intents)
logging.debug("Client instance created")

@client.event
async def on_ready():
    """
    Event listener that is called when the bot successfully connects to Discord.
    It signals that the bot is ready to receive and process commands.
    """
    logging.info("Logged in as {0.user}".format(client))
    logging.info(f"Bot is ready to receive and process commands")

    # Create a counter to track how many guilds/servers the bot is connected to.
    server_count = 0

    # Loop through all servers the bot is connected to
    for guild in client.guilds:
        # Output the ID and name of the server
        logging.info(f"{guild.name} (Name: {guild.id})")

        # Increase the counter
        server_count += 1

    logging.info(f"Bot is running on {server_count} {'server' if server_count == 1 else 'servers'}.")

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
    # Log the message in the console
    logging.debug(f"[{message.channel}] {message.author}: {message.content}")

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
    logging.info("Checking for new emails")
    check_mail()