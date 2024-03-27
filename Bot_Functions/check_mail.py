import os
import imaplib
import email
from email.header import decode_header
import datetime
import fitz

# File to keep track of processed emails
processed_mails = "processed_mails.txt"


def check_mail(current_kw):
    """
    This function checks the email account for new emails with a specific subject line. If a new email is found,
    it downloads any attached PDF files, generates a preview image of the first page, and then deletes the PDF. It
    also marks the email as processed to avoid processing it again in the future.
    """
    # Email account details
    email = os.getenv('EMAIL')
    server = os.getenv('SERVER')
    password = os.getenv('PASSWORD')

    # Connect to the email server
    mail = imaplib.IMAP4_SSL(server)
    try:
        # Login to the email account
        mail.login(email, password)
        # Select the inbox
        mail.select('inbox')

        # Get the current week number
        # current_kw = datetime.date.today().isocalendar()[1]
        # Check if the email has already been processed
        if mail_already_processed(f"WG: Speisenplan KW {current_kw}"):
            print("E-Mail bereits verarbeitet, überspringe...")
            return False

        # Search for new emails with the specific subject line
        typ, data = mail.search(None, f'SUBJECT "Fwd: Speisenplan KW {current_kw}"')
        for num in data[0].split():
            # Fetch the email
            typ, data = mail.fetch(num, '(RFC822)')
            # Parse the email
            msg = email.message_from_bytes(data[0][1])
            # Get the subject line
            subject = decode_header(msg["Subject"])[0][0]

            print(f"Neue E-Mail gefunden: {subject}")

            # Loop through the parts of the email
            for part in msg.walk():
                # Skip if the part is multipart or doesn't have a Content-Disposition header
                if part.get_content_maintype() == 'multipart' or part.get('Content-Disposition') is None:
                    continue

                # Get the filename of the part
                filename = part.get_filename()
                # If the part is a PDF file
                if filename and filename.endswith('.pdf'):
                    # Save the PDF file
                    filepath = filename
                    with open(filepath, 'wb') as f:
                        f.write(part.get_payload(decode=True))
                    print(f"PDF gespeichert: {filepath}")

                    new_name = rename_file(filepath)

                    # Generate a preview image of the first page of the PDF
                    doc = fitz.open(new_name)
                    page = doc.load_page(0)
                    pix = page.get_pixmap()
                    output = f"vorschau_{current_kw}.png"
                    pix.save(output)
                    print(f"PDF-Vorschau gespeichert als {output}")
                    doc.close()
                    # Delete the PDF file
                    os.remove(filepath)
                    # Mark the email as processed
                    mark_mail_as_processed(subject)
                    return True
    finally:
        print("Keine weiteren E-Mails gefunden, beende Verbindung...")
        # Close the connection to the email server
        mail.close()
        mail.logout()


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
