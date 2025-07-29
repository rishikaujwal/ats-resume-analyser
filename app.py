from dotenv import load_dotenv
import streamlit as st
import os
from docx import Document
import PyPDF2
import google.generativeai as genai

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to handle Gemini text input
def get_gemini_response(prompt, resume_text, job_description):
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content([prompt, resume_text, job_description])
    return response.text

# Function for user queries
def get_general_response(query, resume_text):
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content([query, resume_text])
    return response.text

# Extract text from PDF
def input_pdf_setup(uploaded_file):
    pdf_reader = PyPDF2.PdfReader(uploaded_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text() or ""
    return text

# Extract text from DOCX
def input_docx_setup(uploaded_file):
    doc = Document(uploaded_file)
    return "\n".join([para.text for para in doc.paragraphs])

# ------------------ Streamlit App ------------------

st.set_page_config(page_title="ATS Resume Expert")
st.header("🧠 ATS Resume Analyzer (Gemini-powered)")

input_text = st.text_area("📄 Job Description:", key="input")
uploaded_file = st.file_uploader("📤 Upload your resume (PDF or DOCX only):", type=["pdf", "docx"])

resume_text = None

if uploaded_file is not None:
    st.success("✅ Resume Uploaded Successfully")
    if uploaded_file.name.endswith(".pdf"):
        resume_text = input_pdf_setup(uploaded_file)
    elif uploaded_file.name.endswith(".docx"):
        resume_text = input_docx_setup(uploaded_file)
    else:
        st.error("❌ Unsupported file format. Please upload only PDF or DOCX.")

# Prompts
input_prompt1 = """
You are an experienced Technical Human Resource Manager. Review the resume against the job description.
Evaluate whether the candidate fits the role, and highlight strengths and weaknesses accordingly.
"""

input_prompt2 = """
You are an ATS (Applicant Tracking System) scanner. Evaluate the resume vs job description.
Output: 1. Percentage match, 2. Missing keywords, 3. Final thoughts.
"""

input_prompt3 = """
You are an expert HR career coach. Suggest 3–5 actionable improvements to make the resume stronger for this job.
Be specific about keywords, formatting, or achievements. (Short 2–3 line suggestions.)
"""

# Buttons
submit1 = st.button("📋 Tell Me About the Resume")
submit2 = st.button("📊 Match Percentage")
submit3 = st.button("💡 Tips to Improve Resume")

# Responses
if submit1 and resume_text:
    response = get_gemini_response(input_prompt1, resume_text, input_text)
    st.subheader("🔍 Resume Review")
    st.write(response)

elif submit2 and resume_text:
    response = get_gemini_response(input_prompt2, resume_text, input_text)
    st.subheader("📊 Match Report")
    st.write(response)

elif submit3 and resume_text:
    response = get_gemini_response(input_prompt3, resume_text, input_text)
    st.subheader("✨ Resume Improvement Tips")
    st.success(response)

# ------------------ Ask Any Question ------------------
st.markdown("---")
st.subheader("💬 Ask Any Query About Your Resume")
custom_query = st.text_input("Type your question here (e.g., 'What should I add to stand out?')")

if st.button("Respond"):
    if custom_query and resume_text:
        response = get_general_response(custom_query, resume_text)
        st.subheader("🧠 Gemini Says:")
        st.write(response)
    elif not uploaded_file:
        st.warning("⚠️ Please upload a resume first.")
    else:
        st.warning("❗ Please enter your query.")
