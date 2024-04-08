"""
This module contains the weather command for the bot. - WIP
To be implemented in the future.

ToDos:
- Add OPENWEATHERMAP_API_KEY to .env file
- Add weather command to main.py
- Add weather to !essen command in main.py
- Add weekly forcast to task_loop in main.py
"""
import requests

@bot.command(name='wetter')
async def weather(ctx):
    """
    This function sends the current weather in a given city when the 'wetter' command is used.
    """
    await ctx.message.delete
    logging.info(f"Received weather request from {ctx.author.name}")
    api_key = os.getenv('OPENWEATHERMAP_API_KEY')
    logging.info(f"Loaded OpenWeatherMap API key")
    lat = "52.4429081"
    lon = "13.4424778"
    # Coordinates for Annedore-Leber-Berufsbildungswerk
    logging.info(f"Requesting weather data for {city}")
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    complete_url = f"{base_url}&lat={lat}&lon={lon}&appid={api_key}&units=metric&lang=de"

    response = requests.get(complete_url)
    logging.info(f"Received response from OpenWeatherMap API")
    weather_data = response.json()

    logging.debug(f"Response: {weather_data}")
    logging.info(f"Sending weather data to {ctx.author.name}")

    if weather_data["cod"] != "404":
        main = weather_data["main"]
        weather = weather_data["weather"]
        temperature = main["temp"]
        feels_like = main["feels_like"]
        description = weather[0]["description"]

        await ctx.send(f"Die aktuelle Temperatur in {city} beträgt {temperature}°C. Es fühlt sich an wie {feels_like}°C. "
                       f"Die Wetterbeschreibung lautet: {description}.")
    else:
        await ctx.send("Etwas ist schiefgelaufen.")

