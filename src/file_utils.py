from __future__ import annotations
import tempfile
from pathlib import Path
from typing import Optional

from pypdf import PdfReader
import doc2txt

def read_uploaded_file(Uploaded_file) -> str:
    """Read txt, pdf, or docx uploaded from Streamlit."""
    if Uploaded_file is None:
        return ""
    
    suffix = Path(Uploaded_file.name).suffix.lower()

    if suffix == ".txt":
        return Uploaded_file.read().decode("utf-8", errors="ignore")
    
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(Uploaded_file.getvalue())
        tmp_path = tmp.name

    if suffix == ".pdf":
        reader = PdfReader(tmp_path)
        text = []
        for page in reader.pages:
            text.append(page.extract_text() or "")
        return "\n".join(text)

    if suffix == ".docx":
        return doc2txt.process(tmp_path)

    raise ValueError("Unsupported file type. Please upload .txt, .docx, or .pdf")    