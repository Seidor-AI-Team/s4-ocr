# Spec — Crear Plantilla (S4-OCR)

## Contexto

El flujo actual de S4-OCR permite al usuario elegir un **esquema predefinido** (Balance General, Estado de Resultados, etc.) o definir campos manualmente antes de cada extracción. El problema: si un analista siempre extrae los mismos 12 campos de los EEFFs de un determinado fondo, tiene que reingresarlos en cada sesión.

**"Crear Plantilla"** permite guardar ese conjunto de campos con un nombre, para reutilizarlo en futuras extracciones sin reconfigurar nada.

---

## Objetivo

Permitir que el usuario:
1. Defina un conjunto de campos de extracción (nombre, tipo, descripción)
2. Le asigne un nombre a ese conjunto → **plantilla**
3. La plantilla quede disponible en el selector de esquemas de la Pantalla 1
4. Pueda editar o eliminar plantillas existentes

---

## Pantallas

### Modal: Crear / Editar Plantilla

Se accede desde la Pantalla 1 ("Upload + Esquema") mediante un botón **"+ Nueva plantilla"** ubicado junto al selector de esquemas predefinidos.

**Contenido del modal:**

| Elemento | Detalle |
|----------|---------|
| Campo "Nombre de plantilla" | Input texto, requerido, ej: "Balance MIMA 2024" |
| Campo "Descripción" (opcional) | Input texto corto, hint para el usuario |
| Tabla de campos | Igual a la tabla de esquema actual: Nombre del campo / Tipo / Descripción (hint IA) |
| Botón "+ Agregar campo" | Agrega una fila vacía a la tabla |
| Ícono de eliminar fila | Elimina el campo de la lista |
| Botón "Guardar plantilla" | Valida y persiste |
| Botón "Cancelar" | Cierra sin guardar |

**Validaciones antes de guardar:**
- Nombre de plantilla: no vacío, no duplicado
- Al menos 1 campo definido
- Cada campo debe tener nombre no vacío

---

### Selector de Esquemas (Pantalla 1) — cambios

El dropdown/selector actual de esquemas predefinidos debe mostrar dos secciones:

```
── Predefinidos ──
  Balance General
  Estado de Resultados
  Flujo de Caja

── Mis plantillas ──
  Balance MIMA 2024       [✏️ editar] [🗑 eliminar]
  Contrato estándar v2    [✏️ editar] [🗑 eliminar]

  + Nueva plantilla
```

Al seleccionar una plantilla, sus campos se cargan en la tabla de esquema de la misma forma que los esquemas predefinidos.

---

### Flujo: editar plantilla existente

El botón ✏️ junto a cada plantilla del usuario abre el mismo modal con los campos prepoblados. Al guardar, sobreescribe la plantilla (misma ID).

### Flujo: eliminar plantilla

El botón 🗑 muestra una confirmación inline ("¿Eliminar Balance MIMA 2024? Sí / No"). Si confirma, la elimina de la lista.

---

## Modelo de Datos

```typescript
interface Plantilla {
  id: string;           // uuid generado en frontend
  nombre: string;       // "Balance MIMA 2024"
  descripcion?: string;
  campos: CampoEsquema[];
  creadaEn: string;     // ISO date string
}

interface CampoEsquema {
  nombre: string;       // "Total Activos"
  tipo: "numero" | "texto" | "fecha" | "porcentaje";
  descripcion?: string; // hint para la IA
}
```

**Persistencia:** `localStorage` bajo la clave `s4ocr_plantillas`. No requiere backend nuevo para el POC.

---

## API (opcional para persistencia compartida)

Si se necesita compartir plantillas entre usuarios en el mismo hackathon, se puede agregar:

### GET /api/plantillas
Devuelve lista de plantillas del usuario (o todas si no hay auth).

### POST /api/plantillas
```json
{
  "nombre": "Balance MIMA 2024",
  "descripcion": "...",
  "campos": [
    { "nombre": "Total Activos", "tipo": "numero", "descripcion": "..." }
  ]
}
```
Responde con la plantilla creada incluyendo `id` y `creadaEn`.

### PUT /api/plantillas/{id}
Actualiza una plantilla existente.

### DELETE /api/plantillas/{id}
Elimina la plantilla.

> **Decisión para el POC:** implementar solo `localStorage`. Los endpoints son opcionales y solo si el tiempo lo permite.

---

## Criterios de Aceptación

| # | Criterio | Prioridad |
|---|----------|-----------|
| 1 | El usuario puede abrir el modal "Crear plantilla" desde Pantalla 1 | Alta |
| 2 | Al guardar, la plantilla aparece en la sección "Mis plantillas" del selector | Alta |
| 3 | Al seleccionar la plantilla, sus campos se cargan en la tabla de esquema | Alta |
| 4 | La plantilla persiste al recargar la página (localStorage) | Alta |
| 5 | El usuario puede editar una plantilla existente | Media |
| 6 | El usuario puede eliminar una plantilla con confirmación | Media |
| 7 | No se permite guardar una plantilla sin nombre o sin campos | Alta |
| 8 | No se permite guardar dos plantillas con el mismo nombre | Media |

---

## Qué NO hacer (scope del POC)

- No implementar categorías o carpetas de plantillas
- No implementar búsqueda/filtro de plantillas
- No sincronizar plantillas con el servidor (a menos que sobre tiempo)
- No versionar plantillas

---

## Dependencias con spec.md principal

- La tabla de definición de campos (Pantalla 1) ya existe → reutilizarla dentro del modal
- El selector de esquemas predefinidos ya existe → extenderlo, no reemplazarlo
- El formato `CampoEsquema` debe ser compatible con el payload de `POST /api/extract`
