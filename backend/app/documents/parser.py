import fitz  # PyMuPDF
import csv
from io import StringIO
def extract_text_from_pdf(file_bytes: bytes) -> str:
    doc = fitz.open(stream=file_bytes, filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text



def extract_text_from_csv(file_bytes: bytes) -> str:
    text = ""
    content = file_bytes.decode("utf-8")
    reader = csv.reader(StringIO(content))

    for row in reader:
        text += " ".join(row) + "\n"

    return text