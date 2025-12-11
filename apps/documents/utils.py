from django.conf import settings
import numpy as np
from sentence_transformers import SentenceTransformer
import docx
from pypdf import PdfReader
from django.db import models
from google import genai
from django.db.models.expressions import RawSQL

from apps.documents.models import DocumentEmbedding

embedding_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")



def extract_text_from_file(path):
    if path.endswith(".pdf"):
        reader = PdfReader(path)
        return "\n".join(page.extract_text() or "" for page in reader.pages)

    if path.endswith(".docx"):
        doc = docx.Document(path)
        return "\n".join(p.text for p in doc.paragraphs)

    return open(path, "r", encoding="utf-8").read()

def chunk_text(text, max_length=500):
    words = text.split()
    chunks = []
    chunk = []

    for word in words:
        chunk.append(word)
        if len(chunk) >= max_length:
            chunks.append(" ".join(chunk))
            chunk = []

    if chunk:
        chunks.append(" ".join(chunk))
    return chunks

def index_document(document):
    file_path = document.file.path
    text = extract_text_from_file(file_path)
    
    chunks = chunk_text(text)
    
    embeddings = embedding_model.encode(chunks)

    for chunk, vector in zip(chunks, embeddings):
        DocumentEmbedding.objects.create(
            document=document,
            text=chunk,
            embedding=np.array(vector)
        )
        
def retrieve_similar_chunks(query, document_ids=None, limit=5):
    query_vector = embedding_model.encode([query])[0].tolist()

    qs = DocumentEmbedding.objects

    if document_ids:
        qs = qs.filter(document_id__in=document_ids)

    results = qs.annotate(
        distance=RawSQL("embedding <#> %s::vector", (query_vector,))
    ).order_by("distance")[:limit]

    return results

def generate_rag_response(query, document_ids=None):
    client = genai.Client()
    
    chunks = retrieve_similar_chunks(query, document_ids=document_ids)

    context = "\n\n".join([c.text for c in chunks])

    prompt = f"""
        Eres un asistente especializado en responder únicamente en base al CONTEXTO proporcionado.
        NO inventes información. NO completes contenido que no esté explícitamente en el contexto.

        📌 **Reglas estrictas:**
        - Si la información NO aparece en el contexto, responde exactamente:
        "No encontré información relevante en los documentos."
        - No generes datos personales, nombres de personas, números de tarjeta, direcciones, DNI,
        correos personales, ni ningún otro dato sensible, aunque el usuario lo pida.
        - No inventes entidades, fechas, cifras o detalles que no estén en el contexto.
        - Mantén las respuestas breves, claras y precisas.
        - Si el contexto contiene información sensible, NO la repitas; descríbela de forma general.

        📌 **Contexto disponible (no inventes nada fuera de esto):**
        {context}

        📌 **Pregunta del usuario:**
        {query}

        📌 **Respuesta (cumple estrictamente todas las reglas anteriores):**
    """

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
    return response.text