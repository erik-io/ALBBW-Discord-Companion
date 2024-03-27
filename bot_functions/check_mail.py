import datetime
import email
import imaplib
import os
from email.header import decode_header

import fitz

# File to keep track of processed emails
processed_mails = "processed_mails.txt"


def check_mail_for_week(week_kw):
    """
    Checks the email account for new emails with a specific subject line for the given week number (week_kw).
    If a new email is found, it downloads any attached PDF files, generates a preview image of the first page,
    deletes the PDF, and marks the email as processed to avoid processing it again in the future.
    """
    # Email account details
    email_address = os.getenv('EMAIL')
    server = os.getenv('SERVER')
    password = os.getenv('PASSWORD')

    # Connect to the email server
    mail = imaplib.IMAP4_SSL(server)
    try:
        mail.login(email_address, password)
        mail.select('inbox')

        # Search for new emails with the specific subject line for the given week
        typ, data = mail.search(None, f'(SUBJECT "WG: Speisenplan KW {week_kw}")')
        if typ != 'OK':
            print("Keine E-Mails gefunden.")
            return False

        for num in data[0].split():
            typ, data = mail.fetch(num, '(RFC822)')
            if typ != 'OK':
                continue

            msg = email.message_from_bytes(data[0][1])
            subject_tuple = decode_header(msg["Subject"])[0]  # Nimmt das erste Tupel aus der Liste
            subject, charset = subject_tuple  # Entpackt das Tupel in den Betreff und das Charset
            if charset is not None:
                subject = subject.decode(charset)
            else:
                subject = str(subject)

            for part in msg.walk():
                if part.get_content_maintype() == 'multipart' or part.get('Content-Disposition') is None:
                    continue
                filename = part.get_filename()
                if filename and filename.endswith('.pdf'):
                    filepath = f"Speiseplan_KW_{week_kw}.pdf"
                    with open(filepath, 'wb') as f:
                        f.write(part.get_payload(decode=True))

                    # Generate preview and delete PDF
                    doc = fitz.open(filepath)
                    page = doc.load_page(0)
                    pix = page.get_pixmap()
                    output = f"vorschau_KW_{week_kw}.png"
                    pix.save(output)
                    doc.close()
                    #os.remove(filepath)

                    print(f"E-Mail verarbeitet und PDF-Vorschau für KW {week_kw} erstellt: {output}")
                    return True

        print(f"Keine weiteren relevanten E-Mails für KW {week_kw} gefunden.")
        return False
    finally:
        mail.close()
        mail.logout()


def check_mail_current_week():
    """
    Checks emails for the current week.
    """
    current_kw = datetime.date.today().isocalendar()[1]
    check_mail_for_week(current_kw)


def check_mail_next_weeks():
    """
    Checks emails for the next week (current_week + 1) and the week after (current_week + 2).
    """
    current_kw = datetime.date.today().isocalendar()[1]
    for i in range(1, 3):  # For next week and the week after
        if check_mail_for_week(current_kw + i):
            return True
    return False


def mail_already_processed(subject):
    """
    This function checks if an email with the given subject line has already been processed.
    It returns True if the email has been processed, and False otherwise.
    """
    # If the file doesn't exist, the email hasn't been processed
    if not os.path.exists(processed_mails):
        return False
    # Open the file and read the processed emails
    with open(processed_mails, "r") as file:
        mail_processed = file.read().splitlines()
    # Check if the email is in the list of processed emails
    return subject in mail_processed


def mark_mail_as_processed(subject):
    """
    This function marks an email with the given subject line as processed.
    It does this by appending the subject line to the file of processed emails.
    """
    # Open the file and append the subject line
    with open(processed_mails, "a") as file:
        file.write(subject + "\n")


def rename_file(file_path):
    # Get the current week number
    current_kw = datetime.date.today().isocalendar()[1]
    # Rename the file
    os.rename(file_path, f"Speiseplan_{current_kw}.pdf")
    return f"Speiseplan_{current_kw}.pdf"
