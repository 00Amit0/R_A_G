from fastapi import FastAPI
from app.api.endpoints import router as rag_router

app = FastAPI(title="RAG Pipeline with FastAPI + MongoDB")

# include routes
app.include_router(rag_router, prefix="/rag", tags=["rag"])

@app.get("/")
def root():
    return {"status": "ok", "message": "RAG service running"}
