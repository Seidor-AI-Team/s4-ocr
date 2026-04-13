**POC CHARTER - IA LAB GRUPO MACRO**

*Ojo: Se añaden las palabras “Por añadir” **cuando no se tiene certeza/Aun no puede ser definido*

**DEFINICIÓN DEL PROBLEMA**

**PROBLEMA ESPECÍFICO QUE RESOLVEMOS:**

El problema surge al tener que transcribir gran cantidad de datos de documentos que provienen en formato PDF o escaneados a formato Excel y de forma ordenada y estructurada.[^1]

Esta es una tarea repetitiva y demandante en horas hombre, con alta probabilidad de errores involuntarios.[^2]

Se busca desarrollar una herramienta que, sujeto a ciertos parámetros, permita extraer información ordenada y estructurada de documento en formato PDF o escaneados.

Por citar un ejemplo, esta herramienta sería útil para digitar EEFF históricos, obtener data de contratos, memorias, estados de cuenta, entre otros.  [^3]

**PROCESO ACTUAL (AS-IS) - PASO A PASO:**

Secuencia de proceso:

Definir la información que se requiere extraer y la apertura o clasificación que se requiere.

Abrir el pdf o documento scaneado, de forma individual.

Abrir el documento en Excel, en el que se recibirá la información.

Copiar la información, manualmente, desde el pdf o documento escaneado hacia el documento en Excel.

Revisar que los datos hayan sido correctamente imputados. Por ejemplo, en el caso de un dictamen auditado, la suma de activos debe dar el activo total; o, en el caso de un estado de cuenta, el saldo inicial más los movimientos del mes debe arrojar el saldo final.

El tiempo depende que toma realizar está tarea depende de la complejidad de la información que se quiere extraer. En el caso de un EEFF individual, descargar información de 2 años debe tardar aproximadamente 4-5 horas de forma completa, incluyendo notas. En otros casos, podría tomar más tiempo.[^4]

Usualmente esta tarea es ejecutada por practicantes o analistas.

Se utiliza Excel como herramienta y el procedimiento se ejecuta de forma manual.

El dolor es: i) consumo de horas hombres; y, ii) error humano.

**TIEMPO TOTAL PROCESO ACTUAL**: 4-5 horas por EEFF. Comúnmente 24 horas / mes (En el caso de digitar los EE.FF. de 2 empresas por 5 años) aunque puede ser mucho más dependiendo del volumen requerido. 

**FRECUENCIA**: Todos los meses

**COSTO MENSUAL** 24 * 50 = 1200 X 12 = $. 14,400$ por año (Solo enfocándonos en uno de los usos de la herramienta). 

**¿POR QUÉ NO LO HAN RESUELTO ANTES?**

Hasta hace 1-2 años, no existía la tecnología para la extracción de información estructurada desde formatos no estructurados (PDF). A partir del surgimiento de la IA y software especializados, algunas áreas de la compañía han empezado a implementar soluciones específicas que permiten la extracción de datos estructurados. Sin embargo, estas soluciones aun no se han escalado al resto de la compañía. 

En un nivel básico, se ha intentado transcribir información a partir de plataformas de IA (Chatgpt, Gemini, Copilot) pero los resultados no han sido certeros. Actualmente se busca escalar una solución estándar para la extracción de datos estructurados desde formatos no estandarizados. 

**SECCIÓN 2: SOLUCIÓN PROPUESTA (25 min)**

**SOLUCIÓN PROPUESTA - QUÉ CONSTRUIREMOS**

**PROCESO OBJETIVO (TO-BE) - CÓMO SERÁ CON IA:**

Inputs: PDF, Documentos de Word, Excel, etc. o cualquier tipo de archivo con información no estructurada o no estandarizada 

Proceso:

**Paso 1:** Extracción de múltiples sub-imputs: (i) Texto mediante herramientas de OCR disponibles (Tesseract, Amazon Textract, etc) (ii) Tablas estructuradas, etc. [^5]

**Paso 2**: Definir un formato de salida, en la forma de una tabla en Excel con las entradas que se prefieren: [^6]

**Paso ****3****:** Utilizar un lenguaje de LLM (GPT 5.2, Gemini, Copilot) junto con los sub-imputs, para que lea e interprete, basado en instrucciones (“Prompt”) donde el output esperado sea una tabla estructurada (“Structured Outputs”). [^7]

La extracción deberá ser flexible (para permitir la extracción de distintas variables) y que ponga información para auditoria humana (Numero de página de extracción, lenguaje exacto de extracción, etc.)

**Paso ****4****:** Re-hacer el modelo múltiples veces para la identificación de errores, y solo aceptar variables donde la información es igual en cada variable. Si no, revisión humana apoyado de la información para auditoria humana especificado [^8]

Output: Documento Excel con la totalidad de información correcta. 

**TIEMPO TOTAL PROCESO NUEVO**: 5-10 minutos (vs. 4-5 horas antes)

**REDUCCIÓN**: 95%+ en tiempo

**STACK TÉCNICO (para transparencia, no necesitan entender todo):**

**Front-end**:

Streamlit (App web de 1 página con upload de PDF/Excel, campo de “consulta/ejecutar”, preview de resultados en tabla editable) 

**Backend**:

Python 3.11

LLM: GPT 5.2[^9]

**Datos**:

PDF, Word, Excel, etc. de información no estructurada 

Frecuencia de actualización: Por proyecto

**Seguridad**:

Data residency, no training con nuestros datos

Logging completo de queries (audit trail)

Control de acceso por roles

Acceso controlado 

**LO QUE EL POC HARÁ (Alcance SÍ):**

SI tendrá como principal output una tabla estructurada respecto a un formato especificado en el paso 2 

SI manejará información no estándar, o que requiere razonamiento para extraer / conseguir (imputaciones, datos no perfectamente iguales, etc.) [^10]

SI ejecutará checks de data quality (Incluso como paso adicional) 

SI citará fuentes siempre

SI permitirá el funcionamiento en múltiples lenguajes 

SI guardar historial de consultas por usuario [^11]

SI permitirá auditoria humana. 

SI tendrá un nivel muy alto de precisión (>85%) si se permite auditoria humana y múltiples corridas.

**LO QUE EL POC NO HARÁ (Alcance NO - crítico definir límites):**

NO extraerá o convertirá datos fuera de los límites del formato especificado

NO generará informes completos

NO tendrá un nivel muy alto de precisión si se obvia la auditoria humana y múltiples corridas.

**PLAN B SI ALGO FALLA:**

**SECCIÓN 3: DATOS Y FUENTES (20 min)**

**DATOS Y FUENTES - LO MÁS CRÍTICO DEL POC**

**INVENTARIO DE DATOS NECESARIOS:**

**Tabla de Fuentes de Datos**

**DISPONIBILIDAD Y RESPONSABLES (completar ahora):**

Acceso disponible: ✅ SÍ 

Tipo: Terminal (Navegador) 

Credenciales API: ❌ No aplica

Responsable accesos: POR AÑADIR

ETA acceso para SEIDOR: POR AÑADIR

Restricciones de uso: Uso solo interno (VPN / red corporativa). Sin datos sensibles. Máximo “X” ejecuciones por minuto / Máximo “Y” tokens por día 

¿Podemos usar datos en IA?: ✅ SÍ 

**PREPARACIÓN ****DE DATOS (timeline crítico):**[^12]

Para la construcción correcta del POC, serán necesarios: 

Un conjunto de PDFs de EEFF de prueba (valor inicial sugerido: 10 documentos) para validar el funcionamiento de la herramienta.

Idealmente, que esos mismos PDFs ya cuenten con un procesamiento previo de referencia (resultado “ground truth” o esperado) para comparar y verificar la calidad de la IA.

Para la ejecución del POC ya desarrollado, será suficiente con disponer de los documentos EEFF (PDFs) a procesar.

**SEMANA 1 (****Feb ****16-20):**[^13]

☐ Recolección de PDFs de prueba (EEFF): seleccionar ~10 documentos y definir partes relevantes a evaluar (secciones/páginas objetivo). 

☐ Levantamiento de “ground truth”: recopilar resultados de referencia si ya existen (procesamiento previo / Excel esperado). 

☐ Si no existe ground truth: definir plantilla de evaluación (campos/estructura esperada) e iniciar la construcción del ground truth para el set de prueba.

**SEMANA 2 (Feb 23-27):**

 Completar ground truth (si aplica): finalizar resultados esperados para los ~10 PDFs (revisión y validación).

☐ Estandarización y versionado: consolidar PDF’s + ground truth en una carpeta única (nombres, estructura, control de versiones).

☐ Primer dataset funcional disponible: dataset listo para testing (PDF’s + ground truth + criterios de evaluación).

**CALIDAD DE DATOS - CRITERIOS DE ACEPTACIÓN:**

Para que el POC arranque, necesitamos MÍNIMO disponibilidad de documentos fuente no estructurados (PDF’s EEFF) y un conjunto de resultados esperados (“ground truth”) que permita comparar salidas, medir precisión y validar calidad. Si el ground truth no existe, deberá generarse y aprobarse antes de la primera medición.

**SECCIÓN 4: CRITERIOS DE ÉXITO (30 min)**

**CRITERIOS DE ÉXITO - CÓMO MEDIMOS SI FUNCIONA**

**KPIs ****PRIMARIOS ****(Must-have para Go):**[^14]

**KPI #1 – EFICIENCIA (El más importante)**

**KPI #2 – PRECISIÓN (Calidad de respuestas)**

**KPIs SECUNDARIOS (Nice to have):**

**KPI #****3**** – ****Facilidad de uso **

**DECISIÓN GO/NO-GO (La regla clara):**

Al final de la semana 4, evaluamos:

**CALENDARIO DE MEDICIÓN:**

**SECCIÓN 5: EQUIPO Y RESPONSABILIDADES (20 min)**

**Por añadir**

**EQUIPO Y RESPONSABILIDADES - QUIÉN HACE QUÉ**

**ROLES Y CONTACTOS:**

**Sponsor Ejecutivo del POC**

**Champion Operativo (Task Force)**

**Usuarios Piloto**

**Responsabilidades de usuarios piloto**

**Lo que NO se espera**

❌ Que aprendan a programar 

❌ Que resuelvan problemas técnicos 

❌ Que usen la herramienta fuera del horario laboral |

**Punto de Contacto TI / Seguridad**

**5Equipo SEIDOR**

**Gerente de Proyecto**

**Consultor Técnico**

**Consultor Funcional**

**Director de Estrategia IA (Arvind)**

**Disponibilidad SEIDOR**

**SECCIÓN ****7****: TIMELINE Y HITOS (15 min)**

**TIMELINE DETALLADO - SEMANA A SEMANA**

**CALENDARIO COMPLETO:**

**🎨**** CRONOGRAMA DE POC (Inicio: 16 Febrero) — Formato Consultoría Premium**

**Semana 0 — Onsite y Decisión (16–17 Feb 2026)**

**Objetivo: ****Workshop presencial, definición final del POC y firma de compromisos.****.**

**Semana 1 — ****Preparación Técnica y Datos (****18****–22 Feb 2026)**[^15]

**Objetivo: ****Accesos, validación de fuentes, setup de entorno y muestra de datos.**

**Hito Semana 1:**

🔹 Usuarios piloto realizan su **primera consulta real**.

**Semana 2 — ****Desarrollo Core + Onboarding (23–27 Feb 2026)**

**Objetivo: ****Funcionalidades base y primeros usuarios piloto activos.**

**Hito Semana 2:**

🔹 ≥50% usuarios piloto hacen **≥3 consultas reales** en la semana.

**Semana 3 — Uso intensivo + Medición (2–6 Mar)**

**Objetivo: capturar datos reales para evaluar KPIs**

**Hito Semana 3:**

🔹 Time-tracking completo de **≥[N] análisis reales**.

**Semana 4 — ****Uso intensivo + Medición (9–13 Mar 2026)**

**Objetivo: consolidar evidencia + preparar demo para Steering**

**Hito Semana 4:**

🔹 Decisión **Go / No–Go** basada en KPIs primarios.

**Semana 5 — ****Cierre POC y Demo Ejecutiva (16–20 Mar 2026)**

**En función de la decisión**

**Si GO → Escalamiento a MVP**

Kickoff MVP (16 Mar)

Plan de productivización (ambientes, seguridad, usuarios)

**Si NO****-GO → Aprendizaje**

Post-mortem: causa raíz

Decisión: pivotar o pausar IA Lab

**HITOS CRÍTICOS CON RESPONSABLES:**

**RIESGOS DE TIMELINE:**

**SECCIÓN 7: PRESUPUESTO Y RECURSOS (10 min)**

**PRESUPUESTO Y RECURSOS**

**INVERSIÓN ****POC (4 semanas):**[^16]

**SEIDOR - Servicios Profesionales:**

Gerente de Proyecto: 80h × $[rate] = $[X]

Consultor Técnico: 160h × $[rate] = $[Y]

Consultor Funcional: 60h × $[rate] = $[Z]

Director Estrategia (Arvind): 20h × $[rate] = $[W]

TOTAL SEIDOR: $15,000 (fijo)

**Azure - Infraestructura Cloud (4 semanas):**

Azure OpenAI API: ~$800

Pinecone Vector DB: ~$300

Azure Container Apps: ~$200

Storage + Networking: ~$100

TOTAL AZURE: ~$1,400

**Bloomberg - API usage:**

Incluido en licencia actual: $0 adicional

 (Validar con [responsable] que no hay overage charges)

**BCRP - Datos públicos:**

Descarga: $0 (público)

OCR: Incluido en Azure Document Intelligence

**SharePoint - Almacenamiento:**

Incluido en licencia Microsoft actual: $0

────────────────────────────────────────────────────────────────

**INVERSIÓN TOTAL POC: ~$16,400**

**RETORNO ESPERADO AÑO 1: $162,000**

**ROI: 888%**

**PAYBACK: <2 meses**

**RECURSOS GRUPO MACRO (tiempo invertido):**

**Sponsor:**

Calls semanales: 4 × 0.5h = 2h

Demo final + decisión: 2h

TOTAL: 4h en 4 semanas

**Champion:**

Coordinación diaria: 5 días/sem × 0.5h × 4 sem = 10h

Calls semanales: 4 × 0.5h = 2h

TOTAL: 12h en 4 semanas

**Usuarios Piloto (cada uno):**

Onboarding: 3h

Uso semanal: 4 sem × [X]h/sem = [Y]h

Feedback diario: 4 sem × 5 días × 5 min = 1.5h

Survey + sesiones: 2h

**TOTAL POR USUARIO: ~[Y+6.5]h en 4 semanas**

5 Usuarios × [Y+6.5]h = [Total]h

**Frank (TI):**

Setup accesos: 2h

Soporte ad-hoc: ~2h

TOTAL: 4h en 4 semanas

**INVERSIÓN TOTAL TIEMPO GRUPO MACRO: ~[Total]h**

A $[rate promedio]/h = $[Z] en costo de oportunidad

**INVERSIÓN COMBINADA: $16,400 (SEIDOR) + $[Z] (tiempo interno)**

**                    = $[Total] total**

**RETORNO AÑO 1: $162,000**

**ROI REAL: [Calcular]%**

**SI PASA A MVP (Semanas 6-15 post-POC):**

**Inversión adicional estimada:**

SEIDOR desarrollo MVP: $35,000

Azure producción (10 meses): ~$5,000

Expansión a más usuarios: $10,000

TOTAL MVP: ~$50,000

**Timeline MVP: 8-10 semanas**

**Usuarios finales: 15-20 (vs. 5 en POC)**

**ROI MVP año 1: ~600%**

**SECCIÓN 8: FIRMAS Y COMPROMISOS (15 min)**

**FIRMAS Y COMPROMISOS - EL CONTRATO**

Este POC Charter es un acuerdo vinculante entre las partes firmantes.

Al firmar, cada parte se compromete a:

SPONSOR EJECUTIVO SE COMPROMETE A:

✅ Asistir a calls semanales (salvo emergencia justificada)

✅ Desbloquear recursos en <24h cuando sea crítico

✅ Proteger tiempo de usuarios piloto (no sobrecargarlos)

✅ Tomar decisión Go/No-Go basada en datos, no intuición

✅ Comunicar honestamente si algo no está funcionando

Firma: _____________________ Fecha: ___________ 

Nombre: [Nombre completo]     

CHAMPION OPERATIVO SE COMPROMETE A:

✅ Dedicar 1-2h/día a coordinación del POC             

✅ Escalar blockers en <24h si no se resuelven            

✅ Capturar feedback de usuarios diariamente               

✅ Asistir a todas las calls 

Firma: _____________________ Fecha: ___________ 

Nombre: [Nombre completo]     

USUARIOS PILOTO SE COMPROMETEN A: 

✅ Asistir a onboarding obligatorio (Lun 10 Feb, 2-5 PM) 

✅ Usar la herramienta genuinamente [X]h/semana 

✅ Dar feedback honesto (aunque sea negativo)

✅ Participar en time-tracking cuando se solicite

✅ Completar survey final de NPS 

Usuario 1: _________________ Fecha: ___________ 

Usuario 2: _________________ Fecha: ___________ 

Usuario 3: _________________ Fecha: ___________ 

Usuario 4: _________________ Fecha: ___________ 

Usuario 5: _________________ Fecha: ___________ 

FRANK (TI) SE COMPROMETE A: 

✅ Provisión de accesos Azure antes del Vie 20 Feb 

✅ Permisos SharePoint antes del Jue 16Feb 

✅ Bloomberg API credentials antes del Vie 20 Feb 

✅ Respuesta a solicitudes críticas en <24h 

Firma: _____________________ Fecha: ___________ 

Nombre: Frank [Apellido completo] 

SEIDOR SE COMPROMETE A: 

✅ Entregar POC funcional en 4 semanas o explicar por qué no 

✅ Reportar progreso semanalmente con transparencia total 

✅ Escalar riesgos proactivamente (no ocultar problemas) 

✅ Transferir conocimiento genuino (documentación completa) 

✅ Recomendar Go/No-Go basado en datos objetivos 

Firma: _____________________ Fecha: ___________ 

Nombre: [Gerente Proyecto SEIDOR] 

Firma: _____________________ Fecha: ___________ 

Nombre: Arvind Ludhiarich - Director Estrategia IA 

ESTE DOCUMENTO ENTRA EN VIGOR EL LUNES 23 DE FEBRERO, 2026

Copias de este documento se distribuyen a:

Sponsor Ejecutivo (original firmado)

Champion Operativo

Frank (TI)

Gerente Proyecto SEIDOR

Archivo digital compartido (Google Drive / SharePoint)


| Indicador | Razón/especificaciones |
| --- | --- |
| Fujo de caja |  |
| … |  |
|  |  |


| Riesgo | Descripción | Plan B / Mitigación |
| --- | --- | --- |
| Riesgo #1 | Herramienta no alcanza 85% precisión | Mayores checks humanos / mayores corridas / utilizar como información referencial |
| Riesgo #2 | “Pricing” de IA se vuelve inmanejable | Caching agresivo + consultas batch. |
| Riesgo #3 | Usuarios piloto no adoptan (no les gusta la interfaz) | Iteración rápida de UX en semana 2–3 basado en feedback |


| Fuente | Datos específicos | Período | Formato |
| --- | --- | --- | --- |
| Múltiples | PDF’s de EEFF (información no estructurada) | Any | PDF |


| Elemento | Detalle |
| --- | --- |
| Métrica | Tiempo promedio por documento |
| Baseline actual | 5 horas |
| Target POC | 10 minutos |
| Medición | Time-tracking de [N] Análisis reales |
| Responsable de medición | POR AÑADIR |
| Criterio Go / No-Go | • GO: Reducción de tiempo a 20 minutos 
• Revisión: Error, o reducción de tiempo mayor a 20 minutos |


| Elemento | Detalle |
| --- | --- |
| Métrica | % de respuestas verificadas como correctas |
| Target | ≥ 85 % |
| Medición | • Se procesa un EE.FF. ya conocido  
• Usuarios piloto validan 20 respuestas reales durante el uso 
• Promedio de ambas mediciones = score final |
| Responsable | POR AÑADIR |
| Criterio Go / No-Go | • GO: ≥ 85% 
• Revisar prompts: 75%-85% 
• Re-evaluar stack técnico: <75% |


| Elemento | Detalle |
| --- | --- |
| Métrica | % de usuarios con alta satisfacción de uso |
| Target | ≥ 85% |
| Medición | • Se crea un cuestionario de preguntas tipo Likert tanto de facilidad de uso (1-5 que tan “fácil” es) como de satisfacción con los resultados |
| Responsable | POR AÑADIR |
| Criterio Go / No-Go | • GO: ≥ 85% 
• Revisar prompts: 70–85% 
• Re-evaluar stack técnico: <70% |


| Resultado | Condición | Acción requerida |
| --- | --- | --- |
| ✅ GO — Pasar a MVP producción | Si se cumplen todos lo Todos los KPI primarios | Avanzar a desarrollo de MVP |
| ⚠️ ITERAR — 2 semanas adicionales | Si se cumplen 1 de 2 KPIs primarios | Análisis de causa raíz + plan de mejora |
| ❌ PAUSAR / PIVOTAR | Si no se cumplen los KPI’s | Decidir entre re-diseñar el caso o seleccionar otro |


| Semana | Fechas | Actividades principales |
| --- | --- | --- |
| Semana 1 | Por añadir | Onboarding usuarios piloto (1–2h) + guía rápida de uso
Pruebas guiadas con set de EEFF (validación de flujo end-to-end)
Configuración de medición: logging + plantilla de evaluación (baseline) |
| Semana 2 | Por añadir | Uso controlado por usuarios piloto (casos reales)
Captura de feedback y ajustes menores (UX/prompts/parámetros)
Primera medición de precisión (set definido / 20 preguntas o campos) |
| Semana 3 | Por añadir | Uso intensivo + seguimiento de incidencias (estabilidad)
Time-tracking de [N] análisis reales (medición de eficiencia)
Segunda medición de precisión + adopción (consultas/semana). |
| Semana 4 | Por añadir | Demo al Steering Committee 
Presentación de resultados vs. KPIs 
Decisión Go/No-Go |


| Campo | Detalle |
| --- | --- |
| Nombre | [Nombre completo] |
| Cargo | [GG Empresa X] |
| Email | [email] |
| Celular | [número] |
| Responsabilidades | ✓ Revisar progreso semanal (30 min call viernes) 
✓ Desbloquear recursos/accesos en <24h 
✓ Asistir a demo final y tomar decisión Go/No-Go 
✓ Comunicar status a Steering Committee mensual 
✓ Proteger tiempo de usuarios piloto |
| Disponibilidad comprometida | • Viernes 10–10:30 AM: Call semanal 
• WhatsApp/email: Respuesta <4h días hábiles 
• Escalaciones críticas: Llamada inmediata OK |


| Campo | Detalle |
| --- | --- |
| Nombre | [Nombre] |
| Cargo | [Rol en Task Force] |
| Email / Celular | [email] / [número] |
| Responsabilidades | ✓ Coordinación día a día con SEIDOR (WhatsApp) 
✓ Capturar feedback diario de usuarios piloto 
✓ Escalar blockers a Sponsor si no se resuelven en 24h 
✓ Organizar sesiones de prueba con usuarios 
✓ Validar que KPIs se midan correctamente |
| Tiempo comprometido | • 1–2 h/día durante 4 semanas 
• Disponible para llamadas con 2h de anticipación |


| # | Nombre | Cargo | Email | Celular | Compromiso | Disponibilidad | Rol especial |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | [Nombre] | [Cargo] | [Email] | [Celular] | [X] h/semana | ✅ Confirmada | Líder de grupo |
| 2 | [Nombre] | [Cargo] | [Email] | [Celular] | [X] h/semana | ✅ Confirmada | — |
| 3 | [Nombre] | [Cargo] | [Email] | [Celular] | [X] h/semana | ✅ Confirmada | — |
| 4 | [Nombre] | [Cargo] | [Email] | [Celular] | [X] h/semana | ⏳ Pendiente | — |
| 5 | [Nombre] | [Cargo] | [Email] | [Celular] | [X] h/semana | ✅ Confirmada | — |


| Responsabilidades |
| --- |
| ✓ Asistir a onboarding (3h – semana 1) |
| ✓ Usar la herramienta genuinamente |
| ✓ Dar feedback honesto diario (5 min) |
| ✓ Participar en time-tracking cuando se solicite |
| ✓ Completar survey de satisfacción |
| ✓ Asistir a demo final |


| Campo | Detalle |
| --- | --- |
| Nombre | Frank [Apellido] |
| Cargo | [CTO / Head of IT / etc] |
| Email / Celular | [email] / [número] |
| Responsabilidades | ✓ Provisión accesos Azure (Feb 17) 
✓ Permisos SharePoint (Feb 17) 
✓ Bloomberg API credentials (Feb 17) 
✓ Validación de política de seguridad 
✓ Soporte técnico de infraestructura 
✓ Revisión semanal de logs |
| SLA comprometido | • Respuesta a accesos: <24h 
• Blocker crítico: <4h 
• Participación en call semanal: opcional |


| Campo | Detalle |
| --- | --- |
| Nombre | [Nombre] |
| Email / Celular / WhatsApp | [email] / [número] / [número] |
| Responsabilidades | - Coordinación general del POC 
- Reporting semanal al Sponsor 
- Gestión de timeline y entregables 
- Punto de contacto con Champion |


| Campo | Detalle |
| --- | --- |
| Nombre | [Nombre] |
| Email / Celular | [email] / [número] |
| Responsabilidades | - Desarrollo backend & frontend 
- Integraciones Bloomberg/BCRP/SharePoint 
- Resolución de issues técnicos 
- Optimización de performance |


| Campo | Detalle |
| --- | --- |
| Nombre | [Nombre] |
| Email / Celular | [email] / [número] |
| Responsabilidades | - Onboarding usuarios piloto 
- Diseño UX/UI 
- Captura y análisis de feedback 
- Documentación |


| Campo | Detalle |
| --- | --- |
| Nombre | Arvind Ludhiarich |
| Email / Celular | [email] / [número] |
| Responsabilidades | - Revisión estratégica semanal 
- Escalación de riesgos críticos 
- Presentación final a Steering 
- Decisión de pivotes si es necesario |


| Disponibilidad |
| --- |
| • L–V 9 AM – 6 PM (hora Lima) |
| • WhatsApp grupo: respuesta <2h |
| • Emergencias: llamada (<30 min) |
| • Calls semanales: Viernes 10–10:30 AM |


| Fecha | Actividad |
| --- | --- |
| Lun 16 | ✓ Kickoff Día 1 completado |
| Mar 17 | ✓ Kickoff Día 2 completado |
| Mié 18 | SEIDOR: Setup Azure + repositorios |
| Jue 19 | TI: Permisos SharePoint activos |
| Vie 20 | TI: Credenciales Bloomberg API
Responsable: Entrega sample 50 PDFs BCRP |
| Sáb–Dom | SEIDOR: Validación técnica inicial |


| Fecha | Actividad |
| --- | --- |
| Lun 18 | Backend base + integración Bloomberg
Onboarding usuarios piloto (3h) |
| Mar 17 | Inicio indexación SharePoint
Pruebas guiadas (1h) |
| Mié 18 | Validación OCR muestra BCRP
Feedback 30 min |
| Jue 19 | Frontend alpha disponible
Segunda sesión de pruebas |
| Vie 20 | ⚠ Decisión Go/No-Go con BCRP
Call semanal 10–10:30 AM
Ajustes según feedback |
|  |  |


| Fecha | Actividad |
| --- | --- |
| Lun 23 | Funcionalidades core completas
Inicio de uso libre |
| Mar 24 | Monitoring de uso
Feedback diario (Champion) |
| Mié 25 | Iteración UX basada en feedback
Indexación completa BCRP (si aplica) |
| Jue 26 | 1ra medición precisión (20 queries)
Validación indexación SharePoint |
| Vie 27 | Call semanal 10–10:30 AM
Revisión adopción + issues críticos |


| Fecha | Actividad |
| --- | --- |
| Lun 2 | Inicio time-tracking de análisis reales |
| Mar 3 | Optimización performance
Validación time-tracking |
| Mié 4 | Uso intensivo
Medición adopción |
| Jue 5 | 2da medición precisión (30 queries)
Feedback mid-POC |
| Vie 6 | Call semanal 10–10:30 AM
Pre-análisis KPIs |


| Fecha | Actividad |
| --- | --- |
| Lun 9 | Última semana de uso continuo
Compilación de KPIs |
| Mar 10 | Survey NPS
Análisis final de KPIs |
| Mié 11 | Preparación presentación final |
| Jue 12 | Ensayo de demo interna |
| Vie 13 | ⭐ DEMO FINAL (2–4 PM)
• Demo en vivo
• KPIs vs Targets
• Testimonios
• Decisión Go/No-Go |


| HITO | FECHA (Nueva) | RESPONSABLE | CRITERIO DE ÉXITO |
| --- | --- | --- | --- |
| Accesos listos | Lun 16 Feb | Frank | SEIDOR confirma |
| Onboarding OK | Mar 17 Feb | SEIDOR | 100% asistencia |
| Primera consulta | Mié 18 Feb | Usuarios | ≥1 query exitoso |
| Decisión BCRP | Vie 21 Feb | Sponsor | Go/No-Go claro |
| Adopción inicio | Vie 28 Feb | Champion | ≥50% usan 3×/sem |
| Time-tracking | Vie 07 Mar | Usuarios | N análisis OK |
| Survey completo | Mar 10 Mar | Todos | 100% responden |
| Demo Final | Vie 13 Mar | SEIDOR | Presentación OK |
| Decisión final | Vie 13 Mar | Sponsor | Go/No-Go tomado |


| Nivel | Riesgo | Impacto | Mitigación |
| --- | --- | --- | --- |
| 🔴 Crítico | Accesos no listos a tiempo | Retraso de 1 semana en todo el POC | Frank compromete fechas hoy + seguimiento diario |
| 🟡 Medio | Usuarios piloto no asisten al onboarding | Curva de aprendizaje más lenta, menor uso en semana 2 | Sponsor comunica importancia y bloquea agendas ya |
| 🟡 Medio | OCR BCRP falla y se requiere pivotar | Pérdida de 2–3 días en semana 1 | Aplicar Plan B: solo Bloomberg + SharePoint |
| 🟢 Bajo | Usuario piloto enfermo o ausente | No crítico (5 usuarios → 4 suficientes) | Continuar validación con ≥4 usuarios |


---

## Comentarios

[^1]: **Autor:** Arvinder Ludhiarich | **Fecha:** 2026-03-05
  **Contexto:** "El problema surge al tener que transcribir gran cantidad de datos de documentos ..."
  > El problema operativo consiste en la extracción manual de información desde documentos no estructurados (principalmente PDF o documentos escaneados) hacia formatos estructurados (Excel u otros modelos analíticos), proceso que actualmente requiere intervención humana intensiva.

[^2]: **Autor:** Arvinder Ludhiarich | **Fecha:** 2026-03-05
  **Contexto:** "Esta es una tarea repetitiva y demandante en horas hombre, con alta probabilidad..."
  > Reemplazar por: Este proceso presenta tres fricciones operativas principales: 1. Alto consumo de horas analíticas en tareas de bajo valor agregado 2. Riesgo de error humano en la transcripción manual 3. Limitaciones de escalabilidad cuando aumenta el volumen documental

[^3]: **Autor:** Arvinder Ludhiarich | **Fecha:** 2026-03-05
  **Contexto:** "Por citar un ejemplo, esta herramienta sería útil para digitar EEFF históricos, ..."
  > Reemplazar por: Casos de uso representativos donde este problema aparece con mayor frecuencia: - Digitalización de Estados Financieros históricos - Extracción de información de contratos - Procesamiento de memorias corporativas - Captura de datos desde estados de cuenta

[^4]: **Autor:** Arvinder Ludhiarich | **Fecha:** 2026-03-05
  **Contexto:** "El tiempo depende que toma realizar está tarea depende de la complejidad de la i..."
  > Reemplazar por: El tiempo requerido para ejecutar este proceso depende de la complejidad del documento y del nivel de detalle requerido para la extracción.

[^5]: **Autor:** Arvinder Ludhiarich | **Fecha:** 2026-03-05
  **Contexto:** "Paso 1: Extracción de múltiples sub-imputs: (i) Texto mediante herramientas de O..."
  > Reemplazar por: Paso 1 – Procesamiento del documento - Identificación del contenido del documento - Extracción de texto mediante OCR - Identificación de tablas y estructuras semánticas

[^6]: **Autor:** Arvinder Ludhiarich | **Fecha:** 2026-03-05
  **Contexto:** "Paso 2: Definir un formato de salida, en la forma de una tabla en Excel con las ..."
  > Reemplazar por: Paso 2 – Definición de esquema estructurado de salida Se define una plantilla estándar de salida que especifica: - Variables a extraer - Estructura de columnas - Reglas de validación

[^7]: **Autor:** Arvinder Ludhiarich | **Fecha:** 2026-03-05
  **Contexto:** "Paso 3: Utilizar un lenguaje de LLM (GPT 5.2, Gemini, Copilot) junto con los sub..."
  > Reemplazar por: Paso 3 – Interpretación semántica mediante modelo LLM El modelo LLM analiza el contenido extraído y aplica reglas de interpretación para: - identificar variables relevantes - estructurar los datos - completar la tabla definida en el esquema de salida

[^8]: **Autor:** Arvinder Ludhiarich | **Fecha:** 2026-03-05
  **Contexto:** "Paso 4: Re-hacer el modelo múltiples veces para la identificación de errores, y ..."
  > Reemplazar por: Paso 4 – Validación y consistencia Se ejecutan verificaciones automáticas para: - identificar inconsistencias - validar cálculos - marcar variables con baja confianza para revisión humana

[^9]: **Autor:** Arvinder Ludhiarich | **Fecha:** 2026-03-05
  **Contexto:** "LLM: GPT 5.2..."
  > Modelo LLM: GPT-class model o equivalente No conviene amarrar el POC a un modelo específico.

[^10]: **Autor:** Arvinder Ludhiarich | **Fecha:** 2026-03-05
  **Contexto:** "SI manejará información no estándar, o que requiere razonamiento para extraer / ..."
  > Reemplazar por: El sistema será capaz de interpretar documentos con estructura variable o no estandarizada.

[^11]: **Autor:** Arvinder Ludhiarich | **Fecha:** 2026-03-05
  **Contexto:** "SI guardar historial de consultas por usuario..."
  > Reemplazar por: El sistema registrará historial de consultas para fines de auditoría y mejora del modelo.

[^12]: **Autor:** Arvinder Ludhiarich | **Fecha:** 2026-03-05
  **Contexto:** "PREPARACIÓN DE DATOS (timeline crítico):..."
  > Agregar una sub-seccion: Gobernanza de datos Debe incluir: - clasificación de documentos - política de acceso - política de retención

[^13]: **Autor:** Arvinder Ludhiarich | **Fecha:** 2026-03-05
  **Contexto:** "SEMANA 1 (Feb 16-20):..."
  > Corregir timeline

[^14]: **Autor:** Arvinder Ludhiarich | **Fecha:** 2026-03-05
  **Contexto:** "KPIs PRIMARIOS (Must-have para Go):..."
  > Agregar este KPI tb: KPI – Escalabilidad operativa Métrica: Cantidad de documentos procesados por día sin intervención humana.

[^15]: **Autor:** Arvinder Ludhiarich | **Fecha:** 2026-03-05
  **Contexto:** "Semana 1 — Preparación Técnica y Datos (18–22 Feb 2026)..."
  > Corregir los timelines considerando fechas actuales..puede ser desde la tercer semana de marzo

[^16]: **Autor:** Arvinder Ludhiarich | **Fecha:** 2026-03-05
  **Contexto:** "INVERSIÓN POC (4 semanas):..."
  > Falta poner numeros reales aqui
