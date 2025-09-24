from fastapi import APIRouter, UploadFile, File, HTTPException
from app.schemas import UploadIn, UploadOut, ChatIn, ChatOut
from app.core.splitter import chunk_text
from app.core.embeddings import get_embedder
from app.db.mongo import insert_chunk
from app.core.retriever import retrieve
from app.core.generator import get_generator
import uuid
import PyPDF2
import json

router = APIRouter()

@router.post('/upload', response_model=UploadOut)
def upload_doc(payload: UploadIn):
    if not payload.text:
        raise HTTPException(status_code=400, detail='Text is required')
    doc_id = payload.doc_id
    if not doc_id or doc_id.strip() in ["", "string"]:
        doc_id = str(uuid.uuid4())
    chunks = chunk_text(payload.text)
    embedder = get_embedder()
    embeddings = embedder.embed(chunks)
    for chunk_text_content, emb in zip(chunks, embeddings):
        chunk_doc = {
        'doc_id': doc_id,
        'chunk_id': str(uuid.uuid4()),
        'text': chunk_text_content,
        'metadata': payload.metadata or {},
        'embedding': emb.tolist()
        }
        insert_chunk(chunk_doc)
    return {'status': 'ok', 'doc_id': doc_id}

@router.post("/upload_pdf", response_model=UploadOut)
async def upload_pdf(file: UploadFile = File(...), metadata: str = None):
    """
    Upload a PDF file and automatically extract text for the existing upload_doc function.
    """
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported")
    
    # Read the PDF file
    pdf_reader = PyPDF2.PdfReader(file.file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text() + "\n"
    
    if not text.strip():
        raise HTTPException(status_code=400, detail="No text could be extracted from PDF")
    
    # Parse metadata JSON string to dict
    metadata_dict = {}
    if metadata:
        try:
            metadata_dict = json.loads(metadata)
        except json.JSONDecodeError:
            raise HTTPException(status_code=400, detail="metadata must be a valid JSON string")
        
    print("TEXT", text)
    print("metadata", metadata)
    doc_id=str(uuid.uuid4())
    # Prepare payload for existing upload_doc endpoint
    payload = UploadIn(
        text=text,
        metadata=metadata_dict,
        # doc_id=str(uuid.uuid4())
        doc_id=doc_id
    )
    
    print("doc_id", doc_id)
        
    # Call the existing logic
    return upload_doc(payload)



@router.post('/chat', response_model=ChatOut)
def chat(payload: ChatIn):
    top_k = payload.top_k or None
    hits = retrieve(payload.query, top_k=top_k)
    # Build context
    context_texts = [h['doc']['text'] for h in hits]
    context = "---".join(context_texts)
    prompt = f"""
    You are an assistant. Use the context to answer the question.
    
    Context: {context}
    
    Question: {payload.query}
    
    Answer:
    """
    
    gen = get_generator()
    answer = gen.generate(prompt)
    sources = [{'score': h['score'], 'doc_id': h['doc']['doc_id'], 'chunk_id': h['doc']['chunk_id'], 'text': h['doc']['text']} for h in hits]
    return {'answer': answer, 'source_chunks': sources}


# Example for upload endpoint
# "doc_id": "doc123",
#   "text": "FastAPI is a modern, fast web framework for building APIs with Python. It is easy to use and supports asynchronous programming. You can also integrate machine learning models, embeddings, and RAG pipelines.",
#   "metadata": {"author": "Amit", "category": "Tech", "tags": ["FastAPI", "RAG", "Python", "Embeddings"]}