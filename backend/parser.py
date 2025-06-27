from pdfminer.high_level import extract_text as extract_pdf
import docx

def extract_text_from_file(file_path):
    if file_path.endswith(".pdf"):
        return extract_pdf(file_path)
    elif file_path.endswith(".docx"):
        doc = docx.Document(file_path)
        return "\n".join([p.text for p in doc.paragraphs])
    else:
        return "Unsupported file format"
