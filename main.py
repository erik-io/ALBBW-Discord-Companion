import logging

from discord.ext import tasks, commands
from dotenv import load_dotenv

from bot_functions.vegans import *
from bot_functions.check_mail import *
from bot_functions.log import setup_logging
from bot_functions.responses import *

# Set up logging and load environment variables
logging.debug("Environment variables loaded successfully")

# Get the current week number
logging.debug("Getting current date and week number")
current_kw = datetime.date.today().isocalendar()[1]
logging.debug(f"Current week number: {current_kw}")

# Set up intents for the bot
logging.debug("Setting up intents")
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
intents.guilds = True

# Create a bot instance
bot = commands.Bot(command_prefix='!', intents=intents)
logging.debug("Bot instance created")


@bot.command(name='befehle')
async def befehle(ctx):
    """
    This function sends a list of available commands when the 'befehle' command is used.
    """
    logging.info("Befehl wurde von %s ausgeführt", ctx.author)
    await ctx.message.delete()
    await ctx.send(befehlsliste())


@bot.command(name='vorschlag')
async def vorschlag(ctx):
    """
    This function sends a message with command suggestions when the 'vorschläge' command is used.
    """
    admin_ids = [630453809428299777, 224856290545893376]  # (for open source: remove our IDs and replace with yours)
    for admin_id in admin_ids:
        admin = await bot.fetch_user(admin_id)
        if admin:
            await admin.send(f"{ctx.author} wünscht sich eine Funktion für den Bot.: "
                             f"{ctx.message.content.replace('!vorschlag ', '')}\n")
    await ctx.send("Dein Vorschlag wurde an die Admins gesendet. Vielen Dank!", delete_after=5)


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


@bot.command(name='info')
async def info(ctx):
    """
    This function sends cafeteria information when the 'info' command is used.
    """
    await ctx.send(cafeteria_info())


@bot.command(name='essen')
async def essen(ctx):
    """
    This function sends the meal plan when the 'essen' command is used.
    """
    file_path = f"vorschau_KW_{current_kw}.png"
    if os.path.exists(file_path):
        if vegan_meals(current_kw) == 0:
            file = discord.File(file_path)
            await ctx.send(f"Hier ist die Vorschau:",
                           file=file)
        else:
            if can_ping_vegans():
                file = discord.File(file_path)
                await ctx.send(
                    ping_role("Veganer", f"Diese Woche gibt es {vegan_meals(current_kw)} vegane Mahlzeiten.\n"
                                         f"Hier ist die vorschau:", bot), file=file)
                save_last_ping_date()
            else:
                file = discord.File(file_path)
                await ctx.send(f"Hier ist die Vorschau:", file=file)
    else:
        await ctx.send("Es gibt keine Vorschau für diese Woche.")


@bot.command(name='vegan')
async def vegan(ctx):
    """
    This function sends the number of vegan meals for the current week when the 'vegan' command is used.
    """
    await ctx.send(f"In dieser Woche gibt es {vegan_meals(current_kw)} vegane Mahlzeiten.")


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


@bot.command(name='kaffee')
async def kaffee(ctx):
    """
    This function sends the coffee menu when the 'kaffee' command is used.
    """
    await ctx.send(kaffeespezialitaeten())


@bot.command(name='öffnungszeiten')
async def oeffnungszeiten(ctx):
    """
    This function sends the opening hours when the 'öffnungszeiten' command is used.
    """
    await ctx.send(oeffnungszeiten())


@bot.command(name='getränke')
async def getraenke(ctx):
    """
    This function sends the drinks menu when the 'getränke' command is used.
    """
    await ctx.send(getraenke_info())


@bot.event
async def on_ready():
    """
    Event listener that is called when the bot successfully connects to Discord.
    """
    # check_new_mails.start()
    logging.info(f"Logged in as {bot.user}")
    server_count = len(bot.guilds)
    logging.info(f"Bot is ready to receive and process commands on {server_count} servers.")


@bot.event
async def on_message(message):
    """
    The event function 'on_message' responds to every message received on the Discord server the bot has access to.
    Initially, every message along with details about the author and the channel is logged in the console.
    If the message exactly matches "essen", the bot responds in the same channel.
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
    current_kw = datetime.date.today().isocalendar()[1]

    # Überprüft die Mails für die nächsten 3 Wochen
    for i in range(1, 4):
        if check_mail_for_week(current_kw + i):
            file_path = f"vorschau_KW_{current_kw + i}.png"
            if os.path.exists(file_path):
                channel = bot.get_channel(1160946863797719160)  # Ersetzen Sie dies durch Ihre tatsächliche Kanal-ID
                num_vegan_meals = vegan_meals(current_kw + i)
                if num_vegan_meals > 0:
                    file = discord.File(file_path)
                    await channel.send(f"In KW {current_kw + i} gibt es {num_vegan_meals} vegane Mahlzeiten.\nHier ist die Vorschau:", file=file)
                else:
                    await channel.send(f"In KW {current_kw + i} gibt es keine veganen Mahlzeiten.")





def main():
    """
    The main function of the bot. It checks for new emails and then runs the bot.
    """
    setup_logging()
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
