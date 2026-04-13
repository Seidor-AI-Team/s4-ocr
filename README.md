# S4-OCR — Extracción Inteligente de Documentos Financieros

**POC SEIDOR IA Lab · Grupo Macro / MIMA**

Extrae datos estructurados de PDFs financieros (EEFF, contratos, memorias) usando IA.
Reduce el tiempo de transcripción de **4-5 horas a menos de 10 minutos**.

## Setup rápido (5 minutos)

### Backend
```bash
cd backend
cp .env.example .env
# Edita .env y agrega tu OPENAI_API_KEY
pip install -r requirements.txt
python main.py
# API disponible en http://localhost:8004
```

### Frontend
```bash
cd frontend
npm install
npm run dev
# App disponible en http://localhost:5174
```

## Cómo funciona
1. Sube un PDF (estado financiero, contrato, etc.)
2. Selecciona una plantilla o define los campos que quieres extraer
3. La IA extrae los datos y te muestra el resultado con indicador de confianza
4. Edita si algo falla, descarga el CSV

## Stack
- Backend: Python + FastAPI + OpenAI GPT-4o
- Frontend: React + TypeScript + Vite + TailwindCSS v4
- Sin base de datos (todo en memoria)

## Estructura
```
S4-OCR/
├── AGENTS.md       ← Lee esto primero si eres un agente IA
├── docs/spec.md    ← Especificación funcional completa
├── backend/        ← FastAPI API
└── frontend/       ← React app
```

## Para continuar el desarrollo
Ver `AGENTS.md` para las reglas y `docs/spec.md` para los requisitos.
