import PyPDF2
def vegan_meals(current_kw):
    open_file = open(f"Speiseplan_{current_kw}.pdf", "rb")
    pdf = PyPDF2.PdfReader(open_file)

    veg_count = 0

    for page_num in range(len(pdf.pages)):
        page = pdf.pages[page_num]
        text = page.extract_text()
        veg_count += text.lower().count("vegan")
        return veg_count
