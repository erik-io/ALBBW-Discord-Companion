import datetime
import os

import PyPDF2

last_ping_file = "last_vegan_ping.txt"


def vegan_meals(current_kw):
    open_file = open(f'Speiseplan_{current_kw}.pdf', "rb")
    pdf = PyPDF2.PdfReader(open_file)

    veg_count = 0

    for page_num in range(len(pdf.pages)):
        page = pdf.pages[page_num]
        text = page.extract_text()
        veg_count += text.lower().count("vegan")
        return veg_count


def save_last_ping_date():
    """
    Speichert das aktuelle Datum als Datum des letzten Pings in einer Datei.
    """
    with open(last_ping_file, "w") as file:
        file.write(datetime.date.today().isoformat())


def can_ping_vegans():
    """
    Überprüft, ob die "Veganer"-Rolle seit Beginn der aktuellen Woche bereits gepingt wurde.
    Gibt True zurück, wenn ein Ping erlaubt ist, sonst False.
    """
    if not os.path.exists(last_ping_file):
        return True

    with open(last_ping_file, "r") as file:
        last_ping_date = file.read()
        last_ping_date = datetime.datetime.fromisoformat(last_ping_date).date()

    current_date = datetime.date.today()
    if last_ping_date.isocalendar()[1] == current_date.isocalendar()[1] and last_ping_date.year == current_date.year:
        return False
    else:
        return True
