# AGENTS.md — S4-OCR: Extracción Inteligente de Documentos

## Contexto del Proyecto
Eres un agente trabajando en una POC para **Grupo Macro / MIMA**.
El problema: extraer datos estructurados de PDFs financieros (EEFF) manualmente toma 4-5 horas.
La solución: subir un PDF, definir qué datos extraer, y la IA lo hace en minutos con alta precisión.

Este proyecto fue construido durante el **SEIDOR IA Lab Hackathon** (Abril 2026).
El equipo de negocio (no técnico) continuará el desarrollo después del scaffolding inicial.

## Reglas Críticas
- Código simple y directo. **No sobre-ingeniar.**
- UI moderna, limpia, intuitiva — el usuario final no es técnico.
- Priorizar que **funcione** sobre que sea perfecto.
- Todo en un solo proyecto monolítico. No microservicios.
- Los datos mock están en `data/samples/`. Úsalos para probar.
- Si algo es ambiguo en la spec, elige la opción **más simple**.
- Cada respuesta de la IA **siempre** incluye número de página fuente.

## Stack Técnico
- **Backend:** Python 3.11 + FastAPI + uvicorn
- **IA:** OpenAI API (GPT-4o con vision para PDFs) — usar `OPENAI_API_KEY` del .env
- **Frontend:** React 18 + TypeScript + Vite + TailwindCSS v4
- **Sin base de datos** — todo en memoria para el POC

## Estructura del Proyecto
```
S4-OCR/
├── AGENTS.md          # Este archivo — léelo primero
├── README.md          # Setup y contexto
├── docs/spec.md       # Especificación funcional completa
├── backend/
│   ├── main.py        # FastAPI app — punto de entrada
│   ├── extractor.py   # Lógica de extracción con OpenAI
│   ├── validator.py   # Validación de consistencia
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── App.tsx
│   │   ├── components/   # Componentes React
│   │   └── api/          # Llamadas al backend
│   ├── package.json
│   └── vite.config.ts
└── data/
    └── samples/       # PDFs de prueba (EEFF ficticios)
```

## Flujo Principal (para entender qué construir)
1. Usuario sube un PDF
2. Usuario define el esquema de salida (qué campos quiere extraer)
3. Backend extrae con OpenAI → devuelve JSON estructurado
4. Frontend muestra tabla editable con los datos + número de página fuente
5. Usuario puede descargar el resultado como Excel/CSV

## Lo Que Debe Funcionar Antes de Entregar
- [ ] Subir PDF y ver una vista previa
- [ ] Definir campos a extraer (nombre, tipo: número/texto/fecha)
- [ ] Ejecutar extracción y ver resultados en tabla
- [ ] Indicador de confianza por campo
- [ ] Descarga del resultado como CSV

## Lo Que NO Hacer
- No guardar PDFs en disco de forma permanente
- No construir autenticación (es un POC)
- No conectar a bases de datos externas

## Variables de Entorno (.env)
```
OPENAI_API_KEY=sk-...
```

## Para Más Detalle
Ver `docs/spec.md` — es la fuente de verdad para requisitos funcionales.
