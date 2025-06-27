from fastapi import FastAPI, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
import fitz  # PyMuPDF
import re
import io

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def extract_text_from_pdf(file: bytes) -> str:
    doc = fitz.open(stream=file, filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def extract_keywords(text):
    return list(set(re.findall(r'\b[A-Za-z]{4,}\b', text.lower())))

@app.post("/match/")
async def match_resume(resume: UploadFile, job_description: str = Form(...)):
    file_bytes = await resume.read()
    try:
        resume_text = extract_text_from_pdf(file_bytes)
    except Exception as e:
        return {"error": "Failed to extract resume text. Make sure it's a valid PDF."}

    resume_keywords = extract_keywords(resume_text)
    jd_keywords = extract_keywords(job_description)

    missing_skills = list(set(jd_keywords) - set(resume_keywords))
    match_score = round(100 * (1 - len(missing_skills) / max(len(jd_keywords), 1)))
    suggested_keywords = missing_skills[:5]

    improvements = []
    if 'summary' not in resume_text.lower():
        improvements.append("Add a professional summary section.")
    if len(resume_keywords) < 50:
        improvements.append("Include more detailed skills and technologies.")
    if any(word in resume_text.lower() for word in ["hardworking", "good", "nice"]):
        improvements.append("Replace vague words like 'good' with quantifiable achievements.")

    feedback = "Resume is well-aligned!" if match_score > 80 else "Consider adding key skills for better match."

    return {
        "match_score": match_score,
        "resume_skills": list(set(resume_keywords).intersection(jd_keywords)),
        "missing_skills": missing_skills,
        "feedback": feedback,
        "suggested_keywords": suggested_keywords,
        "improvements": improvements
    }
