import PyPDF2

def extract_text_from_pdf(pdf_path):
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
    return text

if __name__ == "__main__":
    pdf_path = "1768227617.pdf"
    text = extract_text_from_pdf(pdf_path)
    print(text)