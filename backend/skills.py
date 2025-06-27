import spacy

SKILL_KEYWORDS = [
    "python", "java", "c++", "javascript", "html", "css", "react",
    "node.js", "sql", "mongodb", "aws", "azure", "docker", "kubernetes",
    "tensorflow", "pytorch", "machine learning", "data analysis",
    "nlp", "git", "flask", "fastapi", "linux", "agile", "scrum"
]

nlp = spacy.load("en_core_web_sm")

def extract_skills(text):
    text = text.lower()
    doc = nlp(text)
    tokens = [token.text for token in doc if not token.is_stop and not token.is_punct]
    found = list(set(skill for skill in SKILL_KEYWORDS if skill in tokens))
    return found
