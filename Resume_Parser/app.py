import streamlit as st
# The parser file contains all the functions needed for extraction
from parser import extract_text_pdf, extract_text_docx, clean_text, extract_skills, extract_education, extract_experience, save_output
import os

# --- Create outputs directory if it doesn't exist ---
if not os.path.exists('outputs'):
    os.makedirs('outputs',exist_ok=True)

st.title("Smart Resume Parser")

# File uploader widget
uploaded_file = st.file_uploader("Upload Resume (PDF or DOCX)", type=["pdf","docx"])

if uploaded_file is not None:
    # 1. Determine file type and extract text
    if uploaded_file.type == "application/pdf":
        text = extract_text_pdf(uploaded_file)
    else:
        text = extract_text_docx(uploaded_file)

    # 2. Clean the text
    text = clean_text(text)
    
    # 3. Extract information
    skills = extract_skills(text)
    education = extract_education(text)
    experience = extract_experience(text)
    
    # 4. Compile result dictionary
    result = {
        "Skills": skills,
        "Education": education,
        "Experience": experience
    }
    
    # 5. Display output on Streamlit
    st.subheader("Parsed Information")
    st.json(result)
    
    # 6. Save output files
    # Use the original file name (without extension) for the output files
    file_name = uploaded_file.name.split('.')[0]
    save_output(result, file_name)
    st.success(f"Output saved as **{file_name}.json** and **{file_name}.csv** in the **outputs** folder.")
