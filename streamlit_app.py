import streamlit as st
import requests
import json

# -----------------------
# Configure API endpoints
# -----------------------
BASE_URL = "http://127.0.0.1:8000/rag"
UPLOAD_URL = f"{BASE_URL}/upload"
UPLOAD_PDF_URL = f"{BASE_URL}/upload_pdf"
CHAT_URL = f"{BASE_URL}/chat"

st.title("RAG System Demo")

# -----------------------
# Upload Text Document
# -----------------------
st.header("1️⃣ Upload Text Document")
text_input = st.text_area("Enter text to upload")
metadata_text = st.text_area("Optional metadata (JSON)")

if st.button("Upload Text"):
    if not text_input.strip():
        st.warning("Please enter some text")
    else:
        try:
            metadata_dict = json.loads(metadata_text) if metadata_text else {}
        except json.JSONDecodeError:
            st.error("Metadata must be valid JSON")
            metadata_dict = {}
        
        payload = {
            "text": text_input,
            "metadata": metadata_dict
        }
        resp = requests.post(UPLOAD_URL, json=payload)
        if resp.status_code == 200:
            st.success(f"Text uploaded successfully! Doc ID: {resp.json().get('doc_id')}")
        else:
            st.error(f"Error: {resp.text}")

# -----------------------
# Upload PDF Document
# -----------------------
st.header("2️⃣ Upload PDF Document")
uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
pdf_metadata = st.text_area("Optional metadata for PDF (JSON)")

if st.button("Upload PDF"):
    if uploaded_file is not None:
        files = {"file": (uploaded_file.name, uploaded_file, "application/pdf")}
        data = {"metadata": pdf_metadata} if pdf_metadata else {}
        resp = requests.post(UPLOAD_PDF_URL, files=files, data=data)
        if resp.status_code == 200:
            st.success(f"PDF uploaded successfully! Doc ID: {resp.json().get('doc_id')}")
        else:
            st.error(f"Error: {resp.text}")
    else:
        st.warning("Please upload a PDF file")

# -----------------------
# Chat
# -----------------------
st.header("3️⃣ Ask a Question")
query = st.text_input("Enter your question")
top_k = st.number_input("Top K results (optional)", min_value=1, max_value=50, value=5)

if st.button("Get Answer") and query.strip():
    payload = {"query": query, "top_k": top_k}
    resp = requests.post(CHAT_URL, json=payload)
    if resp.status_code == 200:
        answer = resp.json().get("answer")
        sources = resp.json().get("source_chunks")
        st.subheader("Answer")
        st.write(answer)
        st.subheader("Source Chunks")
        for s in sources:
            st.write(f"- {s['text'][:150]}... (Doc ID: {s['doc_id']})")
    else:
        st.error(f"Error: {resp.text}")
