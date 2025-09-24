# RAG FastAPI + Streamlit Project

This project is a Retrieval-Augmented Generation (RAG) system built using **FastAPI**, **MongoDB**, and **Streamlit** for the frontend. It allows users to upload documents (PDF or text), generate embeddings, and interact with a chat interface powered by retrieved document chunks.

---

## Features

- **Document Upload**
  - Upload PDF or raw text documents.
  - Automatic chunking and embedding generation using `sentence-transformers`.
  - Metadata support for documents.
  
- **Chat Interface**
  - Ask questions based on uploaded documents.
  - Retrieval of relevant chunks from the database.
  - AI-generated answers using a text generation model.

- **Streamlit UI**
  - Simple web interface for document upload and chat.
  - Real-time interaction with RAG backend.

- **Database**
  - MongoDB stores documents, embeddings, and chunks.
  - Dockerized for easy setup.

---

## Tech Stack

- **Backend:** FastAPI, Python 3.11
- **Frontend:** Streamlit
- **Database:** MongoDB
- **Machine Learning:** sentence-transformers for embeddings, HuggingFace Transformers for generation
- **Deployment:** Docker + Docker Compose

---

## Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/your-repo.git
cd your-repo
