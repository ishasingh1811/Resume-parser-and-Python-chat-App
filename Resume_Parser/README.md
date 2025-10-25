# 🧠 Smart Resume Parser

A Python + Streamlit based app that extracts **Skills**, **Education**, and **Experience** from uploaded resumes (PDF or DOCX).  
It uses **spaCy NLP**, **PyMuPDF**, and **python-docx** for text extraction and processing.

---

## 🚀 Features
✅ Upload resume in **PDF or DOCX** format  
✅ Extract **skills**, **education**, and **experience** automatically  
✅ View structured results instantly on the web app  
✅ Download extracted data in **JSON** and **CSV** formats  
✅ Simple, lightweight, and works locally or on cloud

---

## 🧩 Folder Structure
project_resume/
│
├── app.py # Streamlit UI file
├── parser.py # Resume parsing logic
├── outputs/ # Output JSON & CSV files (auto-created)
├── test_resumes/ # Sample resumes for testing
├── requirements.txt # Python dependencies
└── README.md # Project documentation

---

## ⚙️ Installation Guide

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/your-username/smart-resume-parser.git
cd smart-resume-parser
pip install -r requirements.txt
pip install streamlit spacy pymupdf python-docx pandas
python -m spacy download en_core_web_sm
streamlit run app.py
http://localhost:8501
📂 Output Files

After successful parsing, output files are saved in /outputs folder as:

filename.json

filename.csv
