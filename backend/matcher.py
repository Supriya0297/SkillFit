from sentence_transformers import SentenceTransformer, util
from skills import extract_skills

model = SentenceTransformer('all-MiniLM-L6-v2')

def compute_similarity_and_feedback(resume_text, job_desc):
    # Compute embeddings
    emb_resume = model.encode(resume_text, convert_to_tensor=True)
    emb_jd = model.encode(job_desc, convert_to_tensor=True)
    
    score = util.cos_sim(emb_resume, emb_jd).item() * 100

    # Skill comparison
    resume_skills = extract_skills(resume_text)
    jd_skills = extract_skills(job_desc)
    missing_skills = list(set(jd_skills) - set(resume_skills))

    # Feedback generation
    feedback = f"Match Score: {score:.2f}%. "
    if missing_skills:
        feedback += f"You're missing these key skills: {', '.join(missing_skills)}. Try updating your resume accordingly."
    else:
        feedback += "Excellent! Your resume covers all major job requirements."

    return score, feedback, resume_skills, missing_skills
