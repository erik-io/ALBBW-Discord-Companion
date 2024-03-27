import datetime
import os

import PyPDF2

last_ping_file = "last_vegan_ping.txt"


def vegan_meals(current_kw):
    """
        Counts the number of vegan meals in the current week's menu.
    """
    open_file = open(f'Speiseplan_KW_{current_kw}.pdf', "rb")
    pdf = PyPDF2.PdfReader(open_file)

    veg_count = 0

    for page_num in range(len(pdf.pages)):
        page = pdf.pages[page_num]
        text = page.extract_text()
        veg_count += text.lower().count("vegan")
        return veg_count


def save_last_ping_date():
    """
    Saves the current date as the date of the last ping in a file.
    """
    with open(last_ping_file, "w") as file:
        file.write(datetime.date.today().isoformat())


def can_ping_vegans():
    """
    Checks if the "Vegan" role has already been pinged since the start of the current week.
    Returns True if a ping is allowed, otherwise False.
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
