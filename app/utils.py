import re
import uuid
from typing import Dict, Any

def clean_text(text: str) -> str:
    """Basic text cleanup: remove extra spaces, newlines, etc."""
    return re.sub(r'\s+', ' ', text).strip()

def generate_id() -> str:
    """Generate a unique UUID string."""
    return str(uuid.uuid4())

def format_metadata(metadata: Dict[str, Any]) -> Dict[str, Any]:
    """Ensure metadata keys are strings (Mongo safe)."""
    return {str(k): v for k, v in metadata.items()}
