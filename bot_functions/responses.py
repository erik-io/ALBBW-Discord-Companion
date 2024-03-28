import discord


def befehlsliste():
    """
    This function returns a formatted string containing the coffee specialties and their prices.
    The string is formatted using Markdown syntax for bold and code block elements.
    """
    return (f'__**Befehlsliste:**__\n'
            f'```!info             Zeigt Informationen zur Cafeteria\n'
            f'!essen            Zeigt den Speiseplan\n'
            f'!vegan            Zeigt die Anzahl der veganen Gerichte\n'
            f'!feedback         Sendet Feedback an die Admins\n'
            f'!kaffee           Zeigt das Kaffeeangebot\n'
            f'!getränke         Zeigt das Getränkeangebot\n'
            f'!snacks           Zeigt das Snackangebot\n'
            f'!öffnungszeiten   Zeigt die Öffnungszeiten der Cafeteria\n'
            f'!vorschlag        Sende uns einen Wunsch, den du hast, für unseren Bot.```\n')


# noinspection SpellCheckingInspection
def oeffnungszeiten_info():
    """
    This function returns a formatted string containing the opening hours of the cafeteria.
    The string is formatted using Markdown syntax for bold and code block elements.
    """
    return (f'# Cafeteria\n'
            f'__**Öffnungszeiten:**__\n'
            f'```Montag - Freitag        08:30 Uhr - 15:00 Uhr\n'
            f'Sonderöffnungszeiten    08:30 Uhr - 10.30 Uhr\n'
            f'Mobile Cafeteria        08:30 Uhr - 11:00 Uhr```\n')


# noinspection SpellCheckingInspection
def kaffee_info():
    """
    This function returns a formatted string containing the coffee specialties and their prices.
    The string is formatted using Markdown syntax for bold and code block elements.
    """
    return (f'__**Kaffeespezialitäten:**__\n'
            f'```Milchkaffee                      1,70 €\n'
            f'Heiße Schokolade                 1,70 €\n'
            f'Cappuccino                       1,50 €\n'
            f'Schokoccino                      1,70 €\n'
            f'Latte Macciato                   1,70 €\n'
            f'Espresso                         1,00 €\n'
            f'Doppelter Espresso               1,70 €\n'
            f'Espresso Macchiato               1,30 €\n'
            f'Café Créme                       1,45 €```\n')


# noinspection SpellCheckingInspection
def getraenke_info():
    """
    This function returns a formatted string containing the drinks and their prices.
    The string is formatted using Markdown syntax for bold and code block elements.
    """
    return (f'__**Getränke:**__\n'
            f'```Eistee Orange, 0,5l              1,20 €\n'
            f'Eistee Himbeere, 0,5l            1,20 €\n'
            f'Eistee Apfel, 0,5l               1,20 €\n'
            f'Eistee Multivitamin, 0,5l        1,20 €\n'
            f'H-Drink Vanille, 0,5l            1,30 €\n'
            f'H-Drink Erdbeere, 0,5l           1,30 €\n'
            f'H-Drink Schoko, 0,5l             1,30 €\n'
            f'H-Drink Banane, 0,5l             1,30 €\n'
            f'Capri Sun, 0,2l                  0,65 €\n'
            f'Mineralwasser 0,75l              1,15 €\n'
            f'Coca Cola, 0,33l                 1,40 €\n'
            f'Sprite, 0,33l                    1,40 €\n'
            f'Fanta, 0,5l                      1,70 €\n'
            f'Club-Mate, 0,5l                  2,20 €\n'
            f'Kaffee klein, 0,2 l              1,20 €\n'
            f'Kaffee groß, 0,3 l               1,65 €```\n')


# noinspection SpellCheckingInspection
def snacks_info():
    """
    This function returns a formatted string containing the snacks and their prices.
    The string is formatted using Markdown syntax for bold and code block elements.
    """
    return (f'__**Süßwaren und Snacks:**__\n'
            f'```Cookie, 100 g hell und dunkel    1,80 €\n'
            f'Snickers, 50 g                   0,90 €\n'
            f'Twix, 50 g                       0,90 €\n'
            f'Mars, 51 g                       0,90 €\n'
            f'Leibniz Minis Choco, 125 g       2,10 €\n'
            f'Leibniz Choco 125 g              2,10 €\n'
            f'Pringles, 40 g                   1,40 €\n'
            f'Mentos Frucht, 38 g              0,90 €\n'
            f'Duplo, 18,2 g                    0,40 €\n'
            f'Kinder Riegel, 21 g              0,40 €\n'
            f'Brötchen, Sandwich               1,90 €\n'
            f'Salat, groß                      3,20 €\n'
            f'Salat, klein                     1,70 €\n```')


def cafeteria_info():
    """
    This function returns a formatted string containing the complete cafeteria information. It concatenates the
    strings returned by the oeffnungszeiten_info, kaffee_info, getraenke_info, and snacks_info functions.
    """
    return oeffnungszeiten_info() + kaffee_info() + getraenke_info() + snacks_info()


def oeffnungszeiten():
    """
    This function returns the opening hours of the cafeteria as a formatted string.
    """
    return (f'__**Öffnungszeiten:**__\n'
            f'> Montag - Freitag        08:30 Uhr - 15:00 Uhr\n'
            f'> Sonderöffnungszeiten    08:30 Uhr - 10.30 Uhr\n'
            f'> Mobile Cafeteria        08:30 Uhr - 11:00 Uhr\n')


def kaffeespezialitaeten():
    """
    This function returns the coffee specialties of the cafeteria as a formatted string.
    """
    return (f'__**Kaffeespezialitäten:**__\n'
            f'> Milchkaffee (8,9)         1,70 €\n'
            f'> Heiße Schokolade (8)      1,70 €\n'
            f'> Cappuccino (8,9)          1,50 €\n'
            f'> Schokoccino (8,9)         1,70 €\n'
            f'> Latte Macciato (8,9)      1,70 €\n'
            f'> Espresso (9)              1,00 €\n'
            f'> Doppelter Espresso (9)    1,70 €\n'
            f'> Espresso Macchiato (9)    1,30 €\n'
            f'> Café Créme (9)            1,45 €\n')


async def ping_role(role_name, message, bot):
    """
    This function sends a message to a specific role in a specific channel.
    """
    channel = bot.get_channel(1200385984337027124)  # Beispiel-Channel-ID
    role = discord.utils.get(channel.guild.roles, name=role_name)
    if channel and role:
        await channel.send(f"<@&{role.id}> {message}")
