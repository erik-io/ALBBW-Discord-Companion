import requests
from discord.ext import tasks, commands
from dotenv import load_dotenv

from bot_functions.check_mail import *
from bot_functions.log import *
from bot_functions.responses import *
from bot_functions.vegans import *

# Set up logging and load environment variables
logging.debug("Environment variables loaded successfully")

# Set up intents for the bot
logging.debug("Setting up intents")
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
intents.guilds = True

# Create a bot instance
bot = commands.Bot(command_prefix='!', intents=intents)
logging.debug("Bot instance created")


@bot.command(name='bclear')
async def bclear(ctx):
    """
    This function clears the chat when the 'clear' command is used.
    """
    # (for open source: remove our IDs and replace with yours)
    if ctx.author.id == 630453809428299777 or ctx.author.id == 224856290545893376:
        await ctx.channel.purge(limit=None, bulk=True)
        await ctx.send("Chat wurde gelöscht.", delete_after=5)
    else:
        await ctx.send("Du hast nicht die Berechtigung, diesen Befehl auszuführen.")


@bot.command(name='befehle')
async def befehle(ctx):
    """
    This function sends a list of available commands when the 'befehle' command is used.
    """
    await ctx.message.delete()
    logging.info("Befehl wurde von %s ausgeführt", ctx.author)
    await ctx.send(bot_commands())


@bot.command(name='clear')
async def clear(ctx):
    """
    This function clears the chat when the 'clear' command is used.
    """
    if ctx.author.id == 630453809428299777 or ctx.author.id == 224856290545893376:  # (for open source: remove our IDs)
        await ctx.channel.purge(limit=None, bulk=False)
        await ctx.send("Chat wurde gelöscht.", delete_after=5)
    else:
        await ctx.send("Du hast nicht die Berechtigung, diesen Befehl auszuführen.")


@bot.command(name='essen')
async def essen(ctx):
    """
    This function sends the meal plan when the 'essen' command is used.
    """
    await ctx.message.delete()
    current_kw = get_current_kw()
    # Get the current week number
    logging.debug("Getting current date and week number")
    # always-up-to-date when the command is called
    logging.debug(f"Current week number: {get_current_kw()}")
    file_path = f"vorschau_KW_{get_current_kw()}.png"
    if not mail_already_processed(f"WG: Speisenplan KW {current_kw}"):
        check_mail_current_week()
    else:
        if os.path.exists(file_path):
            if vegan_meals(get_current_kw()) == 0:
                file = discord.File(file_path)
                await ctx.send(f"Hier ist die Vorschau:", file=file)
            else:
                if can_ping_vegans():
                    file = discord.File(file_path)
                    await ctx.send(
                        ping_role("Veganer", f"Diese Woche gibt es {vegan_meals(get_current_kw())} vegane Mahlzeiten.\n"
                                             f"Hier ist die Vorschau:", bot), file=file)
                    save_last_ping_date()
                else:
                    file = discord.File(file_path)
                    await ctx.send(f"Hier ist die Vorschau:", file=file)
            mark_mail_as_processed(f"WG: Speisenplan KW {current_kw}")
        else:
            await ctx.send("Es gibt keine Vorschau für diese Woche.")


@bot.command(name='feedback')
async def feedback(ctx, *, message: str):
    """
    This function sends feedback to the admins when the 'feedback' command is used.
    """
    # delete the message from the user
    await ctx.message.delete()

    admin_ids = [630453809428299777, 224856290545893376]  # Ersetze dies mit den tatsächlichen IDs der Admins
    for admin_id in admin_ids:
        admin = await bot.fetch_user(admin_id)
        if admin:
            await admin.send(f"{message}")
    # Sende die Bestätigungsnachricht als Direktnachricht an den Nutzer
    await ctx.send("Dein Feedback wurde an die Admins gesendet. Vielen Dank!", delete_after=5)


@bot.command(name='getränke')
async def getraenke(ctx):
    """
    This function sends the drinks menu when the 'getränke' command is used.
    """
    await ctx.message.delete()
    await ctx.send(beverage_prices())


@bot.command(name='info')
async def info(ctx):
    """
    This function sends cafeteria information when the 'info' command is used.
    """
    await ctx.message.delete()
    await ctx.send(cafeteria_info())


@bot.command(name='kaffee')
async def kaffee(ctx):
    """
    This function sends the coffee menu when the 'kaffee' command is used.
    """
    await ctx.message.delete()
    await ctx.send(coffee_prices())


@bot.command(name='öffnungszeiten')
async def oeffnungszeiten(ctx):
    """
    This function sends the opening hours when the 'öffnungszeiten' command is used.
    """
    await ctx.message.delete()
    await ctx.send(cafeteria_hours())


@bot.command(name='snacks')
async def snacks(ctx):
    """
    This function sends the snack menu when the 'snacks' command is used.
    """
    await ctx.message.delete()
    await ctx.send(snack_prices())


@bot.command(name='vorschlag')
async def vorschlag(ctx):
    """
    This function sends a message with command suggestions when the 'vorschläge' command is used.
    """
    await ctx.message.delete()
    admin_ids = [630453809428299777, 224856290545893376]  # (for open source: remove our IDs and replace with yours)
    for admin_id in admin_ids:
        admin = await bot.fetch_user(admin_id)
        if admin:
            await admin.send(f"{ctx.author} wünscht sich eine Funktion für den Bot.: "
                             f"{ctx.message.content.replace('!vorschlag ', '')}\n")
    await ctx.send("Dein Vorschlag wurde an die Admins gesendet. Vielen Dank!", delete_after=5)


@bot.command(name='vegan')
async def vegan(ctx):
    """
    This function sends the number of vegan meals for the current week when the 'vegan' command is used.
    """
    await ctx.message.delete()
    await ctx.send(f"In dieser Woche gibt es {vegan_meals(get_current_kw())} vegane Mahlzeiten.")


@bot.command(name='wetter')
async def weather_api(ctx):
    """
    This function sends the current weather in a given city when the 'wetter' command is used.
    """
    await ctx.message.delete()
    logging.info(f"Received weather request from {ctx.author.name}")
    lat = "52.4429081"
    lon = "13.4424778"
    # Coordinates for Annedore-Leber-Berufsbildungswerk/Berlin-Gropiusstadt
    logging.info(f"Requesting weather data for {lat}, {lon}")
    base_url = "https://api.openweathermap.org/data/2.5/weather?"
    complete_url = f"{base_url}&lat={lat}&lon={lon}&appid={OPENWEATHERMAP_API_KEY}&units=metric&lang=de"

    logging.info(f"Received response from OpenWeatherMap API")
    response = requests.get(complete_url)
    weather_data = response.json()

    logging.debug(f"Response: {weather_data}")
    logging.info(f"Sending weather data to {ctx.author.name}")

    if weather_data["cod"] != "404":
        main_data = weather_data["main"]
        weather = weather_data["weather"]
        temperature = main_data["temp"]
        feels_like = main_data["feels_like"]
        description = weather[0]["description"]

        await ctx.send(f"Die aktuelle Temperatur beträgt {temperature}°C. Es fühlt sich an wie {feels_like}°C. "
                       f"Die Wetterbeschreibung lautet: {description}.")
    else:
        await ctx.send("Etwas ist schiefgelaufen.")


@bot.event
async def on_ready():
    """
    Event listener that is called when the bot successfully connects to Discord.
    """
    check_new_mails.start()
    logging.info(f"Logged in as {bot.user}")
    server_count = len(bot.guilds)
    logging.info(f"Bot is ready to receive and process commands on {server_count} servers.")


@bot.event
async def on_message(message):
    """
    The event function 'on_message' responds to every message received on the Discord server the bot has access to.
    Initially, every message along with details about the author and the channel is logged in the console.
    """
    await bot.process_commands(message)
    # Log the message in the console
    logging.debug(f"[{message.channel}] {message.author}: {message.content}")


@tasks.loop(minutes=1440)  # Läuft alle 1440 Minuten (24 Stunden)
async def check_new_mails():
    """
    This function checks for new emails every 1440 minutes (24 hours). If there are new emails, it sends a message to
    a specific channel with the number of vegan meals for the next week and a preview image for the weeks +1, +2, and +3.
    """
    current_kw = get_current_kw()

    # Überprüft die Mails für die nächsten 3 Wochen
    for i in range(1, 4):
        if mail_already_processed(current_kw + i):
            return

        if check_mail_for_week(current_kw + i):
            file_path = f"vorschau_KW_{current_kw + i}.png"
            if os.path.exists(file_path):
                channel = bot.get_channel(1160946863797719160)  # Ersetzen Sie dies durch Ihre tatsächliche Kanal-ID
                num_vegan_meals = vegan_meals(current_kw + i)
                if num_vegan_meals > 0:
                    file = discord.File(file_path)
                    await channel.send(
                        f"In KW {current_kw + i} gibt es {num_vegan_meals} vegane Mahlzeiten.\nHier ist die Vorschau:",
                        file=file)
                    mark_mail_as_processed(file_path)
                else:
                    await channel.send(f"In KW {current_kw + i} gibt es keine veganen Mahlzeiten.")
                    mark_mail_as_processed(file_path)


def get_current_kw():
    """
    This function gets the current week number.
    """
    return datetime.date.today().isocalendar()[1]


def main():
    """
    The main function of the bot. It checks for new emails and then runs the bot.
    """

    check_mail_current_week()

    # Run the bot
    try:
        bot.run(DISCORD_TOKEN)
    except discord.LoginFailure:
        logging.error("Invalid or expired DISCORD_TOKEN")
        exit(1)  # Exit the program with a status code of 1


# Load environment variables from .env file
try:
    logging.info("Loading environment variables from .env file")
    load_dotenv()
    DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
    OPENWEATHERMAP_API_KEY = os.getenv("OPENWEATHERMAP_API_KEY")

    if OPENWEATHERMAP_API_KEY is None:
        raise ValueError("OPENWEATHERMAP_API_KEY is not set")
    else:
        logging.info("OPENWEATHERMAP_API_KEY is set")
        logging.info("Setting up weather command")
    # Check if the Discord token is set
    if DISCORD_TOKEN is None:
        raise ValueError("DISCORD_TOKEN is not set")
    else:
        logging.info("DISCORD_TOKEN is set")
except ValueError as e:
    logging.error(e)  # Log the error message
    exit(1)  # Exit the program with a status code of 1

if __name__ == "__main__":
    main()
