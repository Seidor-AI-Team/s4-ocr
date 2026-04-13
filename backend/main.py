"""
S4-OCR: Extracción Inteligente de Documentos
Backend FastAPI — punto de entrada principal
"""
import os
import uuid
import base64
from typing import List, Optional
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from dotenv import load_dotenv
import io

from openai import AsyncOpenAI
from extractor import extract_fields, pdf_to_text
from validator import validate_consistency

load_dotenv()

# Cliente OpenAI para el endpoint de chat
openai_client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = FastAPI(
    title="S4-OCR — Extracción Inteligente de EEFF",
    description="POC SEIDOR IA Lab — Grupo Macro / MIMA",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:5174", "http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------- Modelos ----------

class SchemaField(BaseModel):
    field: str
    type: str  # number | text | date | percentage
    description: Optional[str] = ""

class ExtractRequest(BaseModel):
    pdf_base64: str
    schema: List[SchemaField]
    filename: Optional[str] = "document.pdf"

class ExtractionResult(BaseModel):
    field: str
    value: str
    confidence: float
    page: int
    source_text: str

class ExtractResponse(BaseModel):
    results: List[ExtractionResult]
    extraction_id: str
    processing_time_seconds: float
    filename: str
    model: str = "gpt-4o"
    tokens_input: int = 0
    tokens_output: int = 0
    tokens_total: int = 0

class ValidateRequest(BaseModel):
    extraction_id: str
    results: List[ExtractionResult]

# ---------- Esquemas predefinidos ----------

PREDEFINED_SCHEMAS = {
    "balance_general": {
        "name": "Balance General",
        "fields": [
            {"field": "Total Activos", "type": "number", "description": "Suma total de todos los activos"},
            {"field": "Activos Corrientes", "type": "number", "description": "Activos convertibles en efectivo en menos de 1 año"},
            {"field": "Activos No Corrientes", "type": "number", "description": "Activos de largo plazo"},
            {"field": "Efectivo y Equivalentes", "type": "number", "description": "Caja, bancos, inversiones de corto plazo"},
            {"field": "Cuentas por Cobrar", "type": "number", "description": "Deudas de clientes por cobrar"},
            {"field": "Inventarios", "type": "number", "description": "Valor del inventario en stock"},
            {"field": "Total Pasivos", "type": "number", "description": "Suma total de obligaciones"},
            {"field": "Pasivos Corrientes", "type": "number", "description": "Deudas a pagar en menos de 1 año"},
            {"field": "Pasivos No Corrientes", "type": "number", "description": "Deudas a largo plazo"},
            {"field": "Patrimonio Neto", "type": "number", "description": "Activos menos pasivos"},
            {"field": "Período", "type": "text", "description": "Fecha o período del estado financiero"},
            {"field": "Moneda", "type": "text", "description": "Moneda del reporte (S/, USD, etc.)"},
        ]
    },
    "estado_resultados": {
        "name": "Estado de Resultados",
        "fields": [
            {"field": "Ingresos Totales", "type": "number", "description": "Ventas netas totales"},
            {"field": "Costo de Ventas", "type": "number", "description": "Costo directo de los bienes vendidos"},
            {"field": "Utilidad Bruta", "type": "number", "description": "Ingresos menos costo de ventas"},
            {"field": "Gastos Operativos", "type": "number", "description": "Gastos de administración y ventas"},
            {"field": "EBITDA", "type": "number", "description": "Utilidad antes de intereses, impuestos, depreciación"},
            {"field": "Utilidad Operativa", "type": "number", "description": "EBIT"},
            {"field": "Utilidad Neta", "type": "number", "description": "Resultado final después de impuestos"},
            {"field": "Impuesto a la Renta", "type": "number", "description": "Impuestos pagados o por pagar"},
            {"field": "Período", "type": "text", "description": "Período cubierto por el estado"},
        ]
    },
    "flujo_caja": {
        "name": "Flujo de Caja",
        "fields": [
            {"field": "Flujo Operativo", "type": "number", "description": "Flujo de caja de operaciones"},
            {"field": "Flujo Inversión", "type": "number", "description": "Flujo de caja de actividades de inversión"},
            {"field": "Flujo Financiamiento", "type": "number", "description": "Flujo de caja de financiamiento"},
            {"field": "Flujo Neto Total", "type": "number", "description": "Suma de los tres flujos"},
            {"field": "Saldo Inicial", "type": "number", "description": "Efectivo al inicio del período"},
            {"field": "Saldo Final", "type": "number", "description": "Efectivo al fin del período"},
            {"field": "Período", "type": "text", "description": "Período cubierto"},
        ]
    }
}

# ---------- Endpoints ----------

@app.get("/")
def root():
    return {"message": "S4-OCR API funcionando", "version": "1.0.0"}

@app.get("/api/schemas")
def get_schemas():
    return {"schemas": PREDEFINED_SCHEMAS}

@app.post("/api/extract", response_model=ExtractResponse)
async def extract(request: ExtractRequest):
    if not os.getenv("OPENAI_API_KEY"):
        raise HTTPException(status_code=500, detail="OPENAI_API_KEY no configurada")

    import time
    start = time.time()

    try:
        pdf_bytes = base64.b64decode(request.pdf_base64)
    except Exception:
        raise HTTPException(status_code=400, detail="PDF en base64 inválido")

    results, usage = await extract_fields(
        pdf_bytes=pdf_bytes,
        schema=request.schema,
        filename=request.filename or "document.pdf",
    )

    elapsed = round(time.time() - start, 2)

    return ExtractResponse(
        results=results,
        extraction_id=str(uuid.uuid4()),
        processing_time_seconds=elapsed,
        filename=request.filename or "document.pdf",
        model=usage.get("model", "gpt-4o"),
        tokens_input=usage.get("tokens_input", 0),
        tokens_output=usage.get("tokens_output", 0),
        tokens_total=usage.get("tokens_total", 0),
    )

@app.post("/api/validate")
def validate(request: ValidateRequest):
    issues = validate_consistency(request.results)
    return {"issues": issues, "is_valid": len(issues) == 0}


# ---------- Chat con el documento ----------

class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    pdf_base64: str
    messages: List[ChatMessage]
    filename: Optional[str] = "document.pdf"

class ChatResponse(BaseModel):
    response: str
    model: str = "gpt-4o"
    tokens_input: int = 0
    tokens_output: int = 0


@app.post("/api/chat", response_model=ChatResponse)
async def chat_with_document(request: ChatRequest):
    """Permite conversar con el documento PDF subido."""
    if not os.getenv("OPENAI_API_KEY"):
        raise HTTPException(status_code=500, detail="OPENAI_API_KEY no configurada")

    try:
        pdf_bytes = base64.b64decode(request.pdf_base64)
    except Exception:
        raise HTTPException(status_code=400, detail="PDF en base64 inválido")

    # Extraer texto del PDF
    pages = pdf_to_text(pdf_bytes)

    if not pages:
        raise HTTPException(status_code=400, detail="No se pudo extraer texto del PDF")

    full_text = "\n\n".join([f"[Página {p}]\n{t}" for p, t in pages.items()])
    text_truncated = full_text[:8000]  # Limitar para no exceder tokens

    # Construir el prompt con contexto
    system_prompt = f"""Eres un asistente experto en análisis de documentos financieros.
Estás analizando el documento: {request.filename}

CONTEXTO DEL DOCUMENTO:
{text_truncated}

INSTRUCCIONES:
- Responde preguntas sobre el contenido del documento
- Si la información no está en el documento, indícalo claramente
- Cita números de página cuando sea relevante
- Sé conciso pero completo en tus respuestas"""

    # Preparar mensajes para OpenAI
    openai_messages = [{"role": "system", "content": system_prompt}]
    for msg in request.messages[-5:]:  # Últimos 5 mensajes para contexto
        openai_messages.append({"role": msg.role, "content": msg.content})

    response = await openai_client.chat.completions.create(
        model="gpt-4o",
        messages=openai_messages,
        temperature=0.3,
        max_tokens=1500,
    )

    return ChatResponse(
        response=response.choices[0].message.content,
        model=response.model,
        tokens_input=response.usage.prompt_tokens if response.usage else 0,
        tokens_output=response.usage.completion_tokens if response.usage else 0,
    )

@app.post("/api/extract-upload")
async def extract_upload(
    file: UploadFile = File(...),
    schema_key: str = "balance_general",
):
    """Endpoint simplificado: sube el archivo directamente (multipart)."""
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Solo se aceptan archivos PDF")

    pdf_bytes = await file.read()
    schema_data = PREDEFINED_SCHEMAS.get(schema_key, PREDEFINED_SCHEMAS["balance_general"])
    schema = [SchemaField(**f) for f in schema_data["fields"]]

    import time
    start = time.time()
    results, usage = await extract_fields(pdf_bytes=pdf_bytes, schema=schema, filename=file.filename)
    elapsed = round(time.time() - start, 2)

    return ExtractResponse(
        results=results,
        extraction_id=str(uuid.uuid4()),
        processing_time_seconds=elapsed,
        filename=file.filename,
        model=usage.get("model", "gpt-4o"),
        tokens_input=usage.get("tokens_input", 0),
        tokens_output=usage.get("tokens_output", 0),
        tokens_total=usage.get("tokens_total", 0),
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8004, reload=True)
