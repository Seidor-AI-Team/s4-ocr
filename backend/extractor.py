"""
extractor.py — Lógica de extracción de datos de PDFs usando OpenAI GPT-4o
"""
import os
import json
import base64
from typing import List
from openai import AsyncOpenAI
from pypdf import PdfReader
from dotenv import load_dotenv
import io

load_dotenv()
client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def pdf_to_text(pdf_bytes: bytes) -> dict:
    """Extrae texto de cada página del PDF.

    Exportada para uso desde main.py (chat endpoint).
    """
    reader = PdfReader(io.BytesIO(pdf_bytes))
    pages = {}
    for i, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""
        if text.strip():
            pages[i] = text
    return pages


async def extract_fields(pdf_bytes: bytes, schema: list, filename: str) -> list:
    """
    Extrae campos estructurados de un PDF usando GPT-4o.
    Retorna lista de ExtractionResult-compatibles.
    """
    pages = pdf_to_text(pdf_bytes)

    if not pages:
        # PDF scaneado sin texto — usar vision
        return await extract_with_vision(pdf_bytes, schema)

    full_text = "\n\n".join([f"[Página {p}]\n{t}" for p, t in pages.items()])

    schema_description = "\n".join([
        f"- {f.field} ({f.type}): {f.description}"
        for f in schema
    ])

    prompt = f"""Eres un experto en extracción de datos financieros.
Analiza el siguiente documento financiero y extrae los campos solicitados.

CAMPOS A EXTRAER:
{schema_description}

INSTRUCCIONES:
1. Para cada campo, encuentra el valor más relevante en el texto
2. Indica tu nivel de confianza (0.0 a 1.0)
3. Indica el número de página donde encontraste el dato
4. Incluye el texto exacto donde encontraste el valor
5. Si no encuentras un campo, usa null como valor

Responde ÚNICAMENTE con JSON válido, sin texto adicional:
{{
  "results": [
    {{
      "field": "nombre del campo",
      "value": "valor encontrado como string",
      "confidence": 0.95,
      "page": 2,
      "source_text": "texto exacto del documento"
    }}
  ]
}}

DOCUMENTO:
{full_text[:12000]}
"""

    response = await client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"},
        temperature=0,
    )

    raw = json.loads(response.choices[0].message.content)
    results = raw.get("results", [])

    # Normalizar
    normalized = []
    for r in results:
        page_val = r.get("page")
        source_text = r.get("source_text")
        normalized.append({
            "field": r.get("field", ""),
            "value": str(r.get("value", "")) if r.get("value") is not None else "No encontrado",
            "confidence": float(r.get("confidence", 0.5)),
            "page": int(page_val) if page_val is not None else 1,
            "source_text": source_text if source_text is not None else "",
        })

    usage_info = {
        "model": response.model,
        "tokens_input": response.usage.prompt_tokens if response.usage else 0,
        "tokens_output": response.usage.completion_tokens if response.usage else 0,
        "tokens_total": response.usage.total_tokens if response.usage else 0,
    }
    return normalized, usage_info


async def extract_with_vision(pdf_bytes: bytes, schema: list) -> list:
    """Para PDFs escaneados (sin texto extraíble) — usa GPT-4o vision."""
    # Convierte primera página a imagen base64
    pdf_b64 = base64.b64encode(pdf_bytes).decode()

    schema_description = "\n".join([
        f"- {f.field} ({f.type}): {f.description}"
        for f in schema
    ])

    prompt = f"""Analiza este documento financiero escaneado y extrae los campos solicitados.

CAMPOS A EXTRAER:
{schema_description}

Responde ÚNICAMENTE con JSON válido:
{{
  "results": [
    {{
      "field": "nombre",
      "value": "valor",
      "confidence": 0.85,
      "page": 1,
      "source_text": "texto visible en el documento"
    }}
  ]
}}"""

    response = await client.chat.completions.create(
        model="gpt-4o",
        messages=[{
            "role": "user",
            "content": [
                {"type": "text", "text": prompt},
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:application/pdf;base64,{pdf_b64}",
                        "detail": "high"
                    }
                }
            ]
        }],
        response_format={"type": "json_object"},
        temperature=0,
    )

    raw = json.loads(response.choices[0].message.content)
    results = raw.get("results", [])

    normalized = []
    for r in results:
        page_val = r.get("page")
        source_text = r.get("source_text")
        normalized.append({
            "field": r.get("field", ""),
            "value": str(r.get("value", "")) if r.get("value") is not None else "No encontrado",
            "confidence": float(r.get("confidence", 0.5)),
            "page": int(page_val) if page_val is not None else 1,
            "source_text": source_text if source_text is not None else "",
        })

    usage_info = {
        "model": response.model,
        "tokens_input": response.usage.prompt_tokens if response.usage else 0,
        "tokens_output": response.usage.completion_tokens if response.usage else 0,
        "tokens_total": response.usage.total_tokens if response.usage else 0,
    }
    return normalized, usage_info
