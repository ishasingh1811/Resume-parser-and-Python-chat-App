import fitz  # PyMuPDF for PDF
from docx import Document # python-docx for DOCX
import re
import spacy
import json
import pandas as pd
import io # Used to handle file objects from Streamlit

# Load the spaCy model
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    print("Downloading en_core_web_sm model...")
    spacy.cli.download("en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")


# --- Text Extraction ---
def extract_text_pdf(uploaded_file):
    """Extracts text from a Streamlit uploaded PDF file object."""
    # Read the file content into a BytesIO object for fitz
    file_bytes = uploaded_file.read()
    doc = fitz.open(stream=file_bytes, filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def extract_text_docx(uploaded_file):
    """Extracts text from a Streamlit uploaded DOCX file object."""
    # Read the file content into an in-memory stream for python-docx
    docx_file_stream = io.BytesIO(uploaded_file.read())
    doc = Document(docx_file_stream)
    text = "\n".join([para.text for para in doc.paragraphs])
    return text

# --- Text Cleaning ---
def clean_text(text):
    """Removes extra whitespace and newlines."""
    # Remove extra spaces and newlines
    text = re.sub(r'\s+', ' ', text)
    text = text.replace('\n', ' ').strip()
    return text

# --- Database/Keywords ---
# NOTE: For a real-world application, this list should be much larger
SKILLS_DB = ['Python', 'Java', 'C++', 'JavaScript', 'HTML', 'CSS', 'Flask', 'Django', 'MySQL', 'Pandas', 'NumPy', 'Wix', 'Excel', 'Data Analysis', 'Machine Learning', 'SQL']


# --- Extract Information ---
def extract_skills(text):
    """Extracts skills based on a keyword database."""
    # Convert text to lower case for case-insensitive matching
    text_lower = text.lower()
    
    # Find all skills from the DB that exist in the text
    found_skills = set()
    for skill in SKILLS_DB:
        if skill.lower() in text_lower:
            found_skills.add(skill)
            
    return sorted(list(found_skills))

def extract_education(text):
    """
    Extracts education-related sentences using keywords and spaCy.
    NOTE: This is basic logic; advanced parsers use NER/custom models.
    """
    doc = nlp(text)
    education_lines = set()
    edu_keywords = ['university', 'college', 'school', 'bachelor', 'master', 'b.tech', 'm.tech', 'b.sc', 'm.sc', 'phd', 'degree', 'diploma']
    
    # Look for sentences containing any education keyword
    for sent in doc.sents:
        if any(keyword in sent.text.lower() for keyword in edu_keywords):
            education_lines.add(sent.text.strip())
            
    return list(education_lines)

def extract_experience(text):
    """
    Extracts experience-related sentences using keywords and spaCy.
    NOTE: This is basic logic; advanced parsers use custom patterns.
    """
    doc = nlp(text)
    experience_lines = set()
    exp_keywords = ['experience', 'internship', 'worked as', 'project', 'company', 'developed', 'led team', 'responsible for']

    # Look for sentences containing any experience keyword
    for sent in doc.sents:
        if any(keyword in sent.text.lower() for keyword in exp_keywords):
            experience_lines.add(sent.text.strip())
            
    return list(experience_lines)

# --- Save Output ---
def save_output(data, filename):
    """Saves the extracted data to JSON and CSV files in the 'outputs' folder."""
    
    # 1. Save as JSON
    try:
        with open(f"outputs/{filename}.json", "w", encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"Error saving JSON: {e}")

    # 2. Save as CSV
    try:
        # Create a DataFrame from the dictionary
        df = pd.DataFrame([data])
        # Expand lists (like skills, education) into a comma-separated string for CSV
        for key in df.columns:
            if isinstance(df[key].iloc[0], list):
                df[key] = df[key].apply(lambda x: "; ".join(x))
                
        df.to_csv(f"outputs/{filename}.csv", index=False, encoding='utf-8')
    except Exception as e:
        print(f"Error saving CSV: {e}")
