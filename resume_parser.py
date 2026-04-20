import pdfplumber
import docx
import re

# ------------------ MAIN FUNCTION ------------------
def extract_text(file):
    text = ""

    try:
        # PDF Handling
        if file.name.endswith(".pdf"):
            with pdfplumber.open(file) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"

        # DOCX Handling
        elif file.name.endswith(".docx"):
            doc = docx.Document(file)
            for para in doc.paragraphs:
                text += para.text + "\n"

        else:
            return ""

        return clean_text(text)

    except Exception as e:
        return ""


# ------------------ CLEANING FUNCTION ------------------
def clean_text(text):
    if not text:
        return ""

    # Convert to lowercase
    text = text.lower()

    # Remove emails
    text = re.sub(r'\S+@\S+', ' ', text)

    # Remove URLs
    text = re.sub(r'http\S+|www\S+', ' ', text)

    # Remove special characters
    text = re.sub(r'[^a-z0-9\s]', ' ', text)

    # Remove extra spaces
    text = re.sub(r'\s+', ' ', text)

    return text.strip()