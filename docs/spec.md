# Spec — S4-OCR: Extracción Inteligente de Documentos (EEFF)

## Problema
Extraer datos de PDFs financieros manualmente toma **4-5 horas por documento**.
- Alta tasa de error humano
- Tarea ejecutada por practicantes/analistas
- Proceso: abrir PDF → copiar a Excel → verificar manualmente

## Solución Target
Una herramienta web donde:
1. Sube un PDF (estado financiero, contrato, memoria, etc.)
2. Defines qué quieres extraer (esquema de salida)
3. La IA extrae los datos en < 5 minutos
4. Revisas, corriges si algo falla, descargas

**Reducción de tiempo esperada: 95%+ (de 4-5h a 5-10 min)**

## Pantallas Requeridas

### Pantalla 1: Upload + Esquema
- Área de drag & drop para subir PDF
- Vista previa del PDF (primera página al menos)
- Definidor de esquema: tabla donde el usuario agrega filas con:
  - `Nombre del campo` (ej: "Total Activos")
  - `Tipo` (número / texto / fecha / porcentaje)
  - `Descripción` (hint para la IA, ej: "Suma de activos corrientes y no corrientes")
- Esquemas predefinidos cargables:
  - Balance General
  - Estado de Resultados
  - Flujo de Caja
- Botón "Extraer Datos"

### Pantalla 2: Resultados
- Tabla con columnas:
  - Campo | Valor Extraído | Confianza (%) | Página Fuente | Texto Original
- Celdas editables para corrección manual
- Indicador visual de confianza: verde (>85%), amarillo (70-85%), rojo (<70%)
- Botón "Re-extraer campos con baja confianza"
- Botón "Descargar CSV"
- Botón "Nueva extracción"

## Esquemas Predefinidos (Mock Data)

### Balance General
| Campo | Tipo |
|-------|------|
| Total Activos | número |
| Activos Corrientes | número |
| Activos No Corrientes | número |
| Total Pasivos | número |
| Pasivos Corrientes | número |
| Pasivos No Corrientes | número |
| Patrimonio Neto | número |
| Cuentas por Cobrar | número |
| Inventarios | número |
| Efectivo y Equivalentes | número |
| Período | texto |
| Moneda | texto |

## API Endpoints

### POST /api/extract
Request:
```json
{
  "pdf_base64": "...",
  "schema": [
    {"field": "Total Activos", "type": "number", "description": "Suma total de activos"},
    ...
  ]
}
```
Response:
```json
{
  "results": [
    {
      "field": "Total Activos",
      "value": "1,234,567",
      "confidence": 0.94,
      "page": 3,
      "source_text": "Total activos S/ 1,234,567"
    }
  ],
  "extraction_id": "uuid",
  "processing_time_seconds": 12.4
}
```

### POST /api/validate
Toma los resultados y verifica consistencia matemática (ej: activos = pasivos + patrimonio).
```json
{"extraction_id": "uuid", "results": [...]}
```

### GET /api/schemas
Devuelve los esquemas predefinidos disponibles.

## Datos Mock
En `data/samples/` hay PDFs de EEFF ficticios para pruebas. Si no hay PDFs reales disponibles, el backend puede operar en modo "demo" con datos hardcodeados.

## Criterios de Éxito
- KPI #1 Eficiencia: < 10 min por documento (baseline: 4-5h)
- KPI #2 Precisión: ≥ 85% de campos correctos
- KPI #3 Usabilidad: Usuario puede completar flujo sin instrucciones

## Prioridad de Construcción
1. Upload de PDF + extracción básica funcionando
2. Tabla de resultados con edición
3. Validación de consistencia
4. Esquemas predefinidos
5. Descarga CSV
