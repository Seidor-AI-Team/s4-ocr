"""
Genera PDFs de muestra ficticios de EEFF peruanos para testing de S4-OCR.
Uso: python generar_muestras.py
Requiere: pip install reportlab
"""
import os
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_RIGHT

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "samples")
os.makedirs(OUTPUT_DIR, exist_ok=True)

styles = getSampleStyleSheet()
title_style = ParagraphStyle("title", parent=styles["Title"], fontSize=14, spaceAfter=6)
subtitle_style = ParagraphStyle("subtitle", parent=styles["Normal"], fontSize=10, spaceAfter=4, textColor=colors.grey)
header_style = ParagraphStyle("header", parent=styles["Heading2"], fontSize=11, spaceBefore=12, spaceAfter=4)
normal = styles["Normal"]

TABLE_STYLE = TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1e40af")),
    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
    ("FONTSIZE", (0, 0), (-1, 0), 9),
    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f0f4ff")]),
    ("FONTSIZE", (0, 1), (-1, -1), 8.5),
    ("ALIGN", (1, 0), (-1, -1), "RIGHT"),
    ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#d1d5db")),
    ("TOPPADDING", (0, 0), (-1, -1), 4),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ("LEFTPADDING", (0, 0), (-1, -1), 8),
    ("RIGHTPADDING", (0, 0), (-1, -1), 8),
    ("FONTNAME", (0, -1), (-1, -1), "Helvetica-Bold"),
    ("BACKGROUND", (0, -1), (-1, -1), colors.HexColor("#dbeafe")),
])


def make_pdf(filename, elements):
    path = os.path.join(OUTPUT_DIR, filename)
    doc = SimpleDocTemplate(path, pagesize=letter,
                            rightMargin=0.75*inch, leftMargin=0.75*inch,
                            topMargin=0.75*inch, bottomMargin=0.75*inch)
    doc.build(elements)
    print(f"  ✓ {filename}")


# ─── PDF 1: Balance General ───────────────────────────────────────────────────
def gen_balance_general():
    elems = []
    elems.append(Paragraph("MACROCONSULT S.A.", title_style))
    elems.append(Paragraph("RUC: 20100123456", subtitle_style))
    elems.append(Paragraph("ESTADO DE SITUACIÓN FINANCIERA (BALANCE GENERAL)", header_style))
    elems.append(Paragraph("Al 31 de Diciembre de 2023 | Moneda: Soles (S/)", subtitle_style))
    elems.append(Spacer(1, 12))

    data_activos = [
        ["ACTIVOS", "2023", "2022"],
        ["ACTIVOS CORRIENTES", "", ""],
        ["Efectivo y Equivalentes de Efectivo", "S/ 8,450,000", "S/ 6,230,000"],
        ["Cuentas por Cobrar Comerciales", "S/ 12,380,000", "S/ 10,150,000"],
        ["Inventarios", "S/ 3,210,000", "S/ 2,890,000"],
        ["Otros Activos Corrientes", "S/ 1,560,000", "S/ 1,240,000"],
        ["TOTAL ACTIVOS CORRIENTES", "S/ 25,600,000", "S/ 20,510,000"],
        ["ACTIVOS NO CORRIENTES", "", ""],
        ["Inmuebles, Maquinaria y Equipo (neto)", "S/ 18,900,000", "S/ 17,400,000"],
        ["Activos Intangibles", "S/ 2,100,000", "S/ 1,800,000"],
        ["Inversiones a Largo Plazo", "S/ 5,400,000", "S/ 4,900,000"],
        ["TOTAL ACTIVOS NO CORRIENTES", "S/ 26,400,000", "S/ 24,100,000"],
        ["TOTAL ACTIVOS", "S/ 52,000,000", "S/ 44,610,000"],
    ]
    t = Table(data_activos, colWidths=[3.5*inch, 1.5*inch, 1.5*inch])
    t.setStyle(TABLE_STYLE)
    elems.append(t)
    elems.append(Spacer(1, 12))

    data_pasivos = [
        ["PASIVOS Y PATRIMONIO", "2023", "2022"],
        ["PASIVOS CORRIENTES", "", ""],
        ["Cuentas por Pagar Comerciales", "S/ 7,200,000", "S/ 6,100,000"],
        ["Obligaciones Financieras CP", "S/ 4,500,000", "S/ 3,800,000"],
        ["Otros Pasivos Corrientes", "S/ 2,300,000", "S/ 1,900,000"],
        ["TOTAL PASIVOS CORRIENTES", "S/ 14,000,000", "S/ 11,800,000"],
        ["PASIVOS NO CORRIENTES", "", ""],
        ["Deudas a Largo Plazo", "S/ 11,200,000", "S/ 10,500,000"],
        ["Provisiones LP", "S/ 1,800,000", "S/ 1,310,000"],
        ["TOTAL PASIVOS NO CORRIENTES", "S/ 13,000,000", "S/ 11,810,000"],
        ["TOTAL PASIVOS", "S/ 27,000,000", "S/ 23,610,000"],
        ["PATRIMONIO NETO", "", ""],
        ["Capital Social", "S/ 15,000,000", "S/ 13,000,000"],
        ["Reserva Legal", "S/ 2,500,000", "S/ 2,100,000"],
        ["Utilidades Retenidas", "S/ 7,500,000", "S/ 5,900,000"],
        ["TOTAL PATRIMONIO NETO", "S/ 25,000,000", "S/ 21,000,000"],
        ["TOTAL PASIVOS + PATRIMONIO", "S/ 52,000,000", "S/ 44,610,000"],
    ]
    t2 = Table(data_pasivos, colWidths=[3.5*inch, 1.5*inch, 1.5*inch])
    t2.setStyle(TABLE_STYLE)
    elems.append(t2)
    elems.append(Spacer(1, 20))
    elems.append(Paragraph(
        "Notas: Los estados financieros han sido preparados de acuerdo con las Normas Internacionales de "
        "Información Financiera (NIIF) adoptadas en el Perú. Las cifras están expresadas en miles de Soles.",
        ParagraphStyle("nota", parent=normal, fontSize=7, textColor=colors.grey)
    ))

    make_pdf("balance_general_macroconsult_2023.pdf", elems)


# ─── PDF 2: Estado de Resultados ─────────────────────────────────────────────
def gen_estado_resultados():
    elems = []
    elems.append(Paragraph("MACROCAPITALES S.A.C.", title_style))
    elems.append(Paragraph("RUC: 20456789012", subtitle_style))
    elems.append(Paragraph("ESTADO DE RESULTADOS INTEGRALES", header_style))
    elems.append(Paragraph("Por el año terminado al 31 de Diciembre de 2023 | Moneda: USD", subtitle_style))
    elems.append(Spacer(1, 12))

    data = [
        ["CONCEPTO", "2023", "2022"],
        ["INGRESOS", "", ""],
        ["Ingresos por Gestión de Fondos", "USD 18,500,000", "USD 15,200,000"],
        ["Comisiones de Administración", "USD 3,200,000", "USD 2,800,000"],
        ["Otros Ingresos Operativos", "USD 900,000", "USD 650,000"],
        ["INGRESOS TOTALES", "USD 22,600,000", "USD 18,650,000"],
        ["COSTOS Y GASTOS", "", ""],
        ["Costo de Servicios Prestados", "USD 8,400,000", "USD 7,200,000"],
        ["UTILIDAD BRUTA", "USD 14,200,000", "USD 11,450,000"],
        ["Gastos de Administración", "USD 3,100,000", "USD 2,700,000"],
        ["Gastos de Ventas y Marketing", "USD 1,200,000", "USD 980,000"],
        ["Depreciación y Amortización", "USD 650,000", "USD 590,000"],
        ["GASTOS OPERATIVOS", "USD 4,950,000", "USD 4,270,000"],
        ["EBITDA", "USD 9,900,000", "USD 7,770,000"],
        ["UTILIDAD OPERATIVA (EBIT)", "USD 9,250,000", "USD 7,180,000"],
        ["Ingresos Financieros", "USD 420,000", "USD 310,000"],
        ["Gastos Financieros", "USD (680,000)", "USD (590,000)"],
        ["UTILIDAD ANTES DE IMPUESTOS", "USD 8,990,000", "USD 6,900,000"],
        ["Impuesto a la Renta (29.5%)", "USD (2,652,000)", "USD (2,035,500)"],
        ["UTILIDAD NETA DEL EJERCICIO", "USD 6,338,000", "USD 4,864,500"],
    ]
    t = Table(data, colWidths=[3.5*inch, 1.5*inch, 1.5*inch])
    t.setStyle(TABLE_STYLE)
    elems.append(t)
    elems.append(Spacer(1, 20))
    elems.append(Paragraph("Período: Enero - Diciembre 2023", subtitle_style))
    elems.append(Paragraph(
        "Los resultados del ejercicio 2023 muestran un crecimiento del 30.3% en ingresos totales "
        "respecto al ejercicio anterior, impulsado principalmente por el incremento en activos "
        "bajo gestión (AUM) y la captación de nuevos mandatos institucionales.",
        ParagraphStyle("nota", parent=normal, fontSize=8)
    ))

    make_pdf("estado_resultados_macrocapitales_2023.pdf", elems)


# ─── PDF 3: Flujo de Caja ─────────────────────────────────────────────────────
def gen_flujo_caja():
    elems = []
    elems.append(Paragraph("MACROINVEST S.A.", title_style))
    elems.append(Paragraph("RUC: 20789012345", subtitle_style))
    elems.append(Paragraph("ESTADO DE FLUJOS DE EFECTIVO", header_style))
    elems.append(Paragraph("Por el período enero–diciembre 2023 | Moneda: Soles (S/)", subtitle_style))
    elems.append(Spacer(1, 12))

    data = [
        ["CONCEPTO", "2023", "2022"],
        ["A. ACTIVIDADES DE OPERACIÓN", "", ""],
        ["Utilidad Neta del Ejercicio", "S/ 4,200,000", "S/ 3,100,000"],
        ["(+) Depreciación y Amortización", "S/ 890,000", "S/ 820,000"],
        ["(+/-) Cambios en Capital de Trabajo", "S/ (450,000)", "S/ 230,000"],
        ["(+/-) Variación en Cuentas por Cobrar", "S/ (780,000)", "S/ (320,000)"],
        ["(+/-) Variación en Inventarios", "S/ (120,000)", "S/ 80,000"],
        ["(+/-) Variación en Cuentas por Pagar", "S/ 560,000", "S/ 410,000"],
        ["FLUJO OPERATIVO NETO", "S/ 4,300,000", "S/ 4,320,000"],
        ["B. ACTIVIDADES DE INVERSIÓN", "", ""],
        ["Compra de Activos Fijos", "S/ (2,100,000)", "S/ (1,800,000)"],
        ["Adquisición de Intangibles", "S/ (350,000)", "S/ (280,000)"],
        ["Ingresos por Venta de Activos", "S/ 180,000", "S/ 0"],
        ["FLUJO INVERSIÓN NETO", "S/ (2,270,000)", "S/ (2,080,000)"],
        ["C. ACTIVIDADES DE FINANCIAMIENTO", "", ""],
        ["Préstamos Bancarios Recibidos", "S/ 3,000,000", "S/ 2,500,000"],
        ["Amortización de Deuda", "S/ (2,400,000)", "S/ (1,900,000)"],
        ["Dividendos Pagados", "S/ (1,200,000)", "S/ (800,000)"],
        ["FLUJO FINANCIAMIENTO NETO", "S/ (600,000)", "S/ (200,000)"],
        ["FLUJO NETO TOTAL", "S/ 1,430,000", "S/ 2,040,000"],
        ["SALDO INICIAL DE EFECTIVO", "S/ 6,230,000", "S/ 4,190,000"],
        ["SALDO FINAL DE EFECTIVO", "S/ 7,660,000", "S/ 6,230,000"],
    ]
    t = Table(data, colWidths=[3.5*inch, 1.5*inch, 1.5*inch])
    t.setStyle(TABLE_STYLE)
    elems.append(t)
    elems.append(Spacer(1, 20))
    elems.append(Paragraph(
        "Nota: El flujo de caja operativo se mantiene positivo, reflejando la solidez del modelo de negocio. "
        "El incremento en inversiones corresponde al plan de expansión aprobado por Directorio en Q1 2023.",
        ParagraphStyle("nota", parent=normal, fontSize=8)
    ))

    make_pdf("flujo_caja_macroinvest_2023.pdf", elems)


if __name__ == "__main__":
    print("Generando PDFs de muestra para S4-OCR...")
    gen_balance_general()
    gen_estado_resultados()
    gen_flujo_caja()
    print(f"\n✅ PDFs generados en: {OUTPUT_DIR}")
