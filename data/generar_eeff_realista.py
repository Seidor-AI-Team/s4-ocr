"""
Genera PDFs realistas de Estados Financieros para la demo de S4-OCR.
Simula documentos reales de empresas peruanas del Grupo Macro.
"""
from fpdf import FPDF
import os

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "samples")


class EEFFReport(FPDF):
    def header(self):
        self.set_font("Helvetica", "B", 10)
        self.cell(0, 6, self.company_name, align="R", new_x="LMARGIN", new_y="NEXT")
        self.set_font("Helvetica", "", 8)
        self.cell(0, 5, f"RUC: {self.ruc}", align="R", new_x="LMARGIN", new_y="NEXT")
        self.ln(2)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 7)
        self.cell(0, 10, f"Pagina {self.page_no()}/{{nb}}", align="C")

    def add_title(self, title, subtitle=""):
        self.set_font("Helvetica", "B", 14)
        self.cell(0, 10, title, align="C", new_x="LMARGIN", new_y="NEXT")
        if subtitle:
            self.set_font("Helvetica", "", 10)
            self.cell(0, 7, subtitle, align="C", new_x="LMARGIN", new_y="NEXT")
        self.ln(5)

    def add_table(self, headers, rows, col_widths=None):
        if col_widths is None:
            col_widths = [self.epw / len(headers)] * len(headers)

        # Header
        self.set_font("Helvetica", "B", 8)
        self.set_fill_color(40, 60, 100)
        self.set_text_color(255, 255, 255)
        for i, h in enumerate(headers):
            self.cell(col_widths[i], 7, h, border=1, fill=True, align="C")
        self.ln()

        # Rows
        self.set_font("Helvetica", "", 8)
        self.set_text_color(0, 0, 0)
        fill = False
        for row in rows:
            if fill:
                self.set_fill_color(240, 240, 245)
            else:
                self.set_fill_color(255, 255, 255)
            for i, val in enumerate(row):
                align = "L" if i == 0 else "R"
                self.cell(col_widths[i], 6, str(val), border=1, fill=True, align=align)
            self.ln()
            fill = not fill

    def add_section(self, title):
        self.ln(3)
        self.set_font("Helvetica", "B", 10)
        self.set_fill_color(230, 233, 240)
        self.cell(0, 7, f"  {title}", fill=True, new_x="LMARGIN", new_y="NEXT")
        self.ln(2)

    def add_notes(self, notes):
        self.ln(3)
        self.set_font("Helvetica", "B", 9)
        self.cell(0, 6, "Notas a los Estados Financieros", new_x="LMARGIN", new_y="NEXT")
        self.set_font("Helvetica", "", 8)
        for i, note in enumerate(notes, 1):
            self.multi_cell(0, 5, f"{i}. {note}")
            self.ln(1)


def fmt(n):
    """Format number as S/ thousands with commas."""
    if isinstance(n, str):
        return n
    return f"{n:,.0f}"


def generate_balance_general():
    pdf = EEFFReport()
    pdf.company_name = "MACROCONSULT S.A."
    pdf.ruc = "20100123456"
    pdf.alias_nb_pages()
    pdf.add_page()

    pdf.add_title(
        "ESTADO DE SITUACION FINANCIERA",
        "Al 31 de diciembre de 2024 y 2023 (En miles de Soles)"
    )

    # ACTIVOS
    pdf.add_section("ACTIVOS")
    headers = ["Cuenta", "2024", "2023", "Variacion %"]
    w = [pdf.epw * 0.45, pdf.epw * 0.18, pdf.epw * 0.18, pdf.epw * 0.19]

    activo_corriente = [
        ("Efectivo y equivalentes de efectivo", 12450, 9870, "26.1%"),
        ("Cuentas por cobrar comerciales", 8320, 7150, "16.4%"),
        ("Cuentas por cobrar a partes relacionadas", 1540, 1280, "20.3%"),
        ("Otras cuentas por cobrar", 2180, 1950, "11.8%"),
        ("Gastos pagados por anticipado", 890, 720, "23.6%"),
        ("TOTAL ACTIVO CORRIENTE", 25380, 20970, "21.0%"),
    ]
    rows = [(r[0], fmt(r[1]), fmt(r[2]), r[3]) for r in activo_corriente]
    pdf.set_font("Helvetica", "B", 9)
    pdf.cell(0, 6, "Activo Corriente", new_x="LMARGIN", new_y="NEXT")
    pdf.add_table(headers, rows, w)

    activo_no_corriente = [
        ("Propiedades, planta y equipo (neto)", 15670, 14230, "10.1%"),
        ("Activos intangibles (neto)", 3420, 2890, "18.3%"),
        ("Activo por derecho de uso", 4560, 4120, "10.7%"),
        ("Inversiones en subsidiarias", 8900, 8900, "0.0%"),
        ("Otros activos no corrientes", 1230, 980, "25.5%"),
        ("TOTAL ACTIVO NO CORRIENTE", 33780, 31120, "8.5%"),
    ]
    rows = [(r[0], fmt(r[1]), fmt(r[2]), r[3]) for r in activo_no_corriente]
    pdf.ln(3)
    pdf.set_font("Helvetica", "B", 9)
    pdf.cell(0, 6, "Activo No Corriente", new_x="LMARGIN", new_y="NEXT")
    pdf.add_table(headers, rows, w)

    pdf.ln(2)
    pdf.set_font("Helvetica", "B", 10)
    pdf.cell(0, 7, f"TOTAL ACTIVOS:  S/ {fmt(59160)}  (2023: S/ {fmt(52090)})", new_x="LMARGIN", new_y="NEXT")

    # PASIVOS
    pdf.add_section("PASIVOS Y PATRIMONIO")
    pasivo_corriente = [
        ("Cuentas por pagar comerciales", 5430, 4870, "11.5%"),
        ("Remuneraciones y participaciones", 3210, 2890, "11.1%"),
        ("Tributos por pagar", 1870, 1540, "21.4%"),
        ("Provisiones", 2100, 1800, "16.7%"),
        ("Parte corriente deuda largo plazo", 3500, 3500, "0.0%"),
        ("TOTAL PASIVO CORRIENTE", 16110, 14600, "10.3%"),
    ]
    rows = [(r[0], fmt(r[1]), fmt(r[2]), r[3]) for r in pasivo_corriente]
    pdf.set_font("Helvetica", "B", 9)
    pdf.cell(0, 6, "Pasivo Corriente", new_x="LMARGIN", new_y="NEXT")
    pdf.add_table(headers, rows, w)

    pasivo_no_corriente = [
        ("Obligaciones financieras LP", 8500, 9200, "-7.6%"),
        ("Pasivo por derecho de uso LP", 3200, 3800, "-15.8%"),
        ("Pasivo diferido", 1450, 1320, "9.8%"),
        ("TOTAL PASIVO NO CORRIENTE", 13150, 14320, "-8.2%"),
    ]
    rows = [(r[0], fmt(r[1]), fmt(r[2]), r[3]) for r in pasivo_no_corriente]
    pdf.ln(3)
    pdf.set_font("Helvetica", "B", 9)
    pdf.cell(0, 6, "Pasivo No Corriente", new_x="LMARGIN", new_y="NEXT")
    pdf.add_table(headers, rows, w)

    patrimonio = [
        ("Capital social", 15000, 15000, "0.0%"),
        ("Reserva legal", 3000, 2500, "20.0%"),
        ("Resultados acumulados", 11900, 5670, "109.9%"),
        ("TOTAL PATRIMONIO", 29900, 23170, "29.1%"),
    ]
    rows = [(r[0], fmt(r[1]), fmt(r[2]), r[3]) for r in patrimonio]
    pdf.ln(3)
    pdf.set_font("Helvetica", "B", 9)
    pdf.cell(0, 6, "Patrimonio Neto", new_x="LMARGIN", new_y="NEXT")
    pdf.add_table(headers, rows, w)

    pdf.ln(2)
    pdf.set_font("Helvetica", "B", 10)
    pdf.cell(0, 7, f"TOTAL PASIVO + PATRIMONIO:  S/ {fmt(59160)}  (2023: S/ {fmt(52090)})", new_x="LMARGIN", new_y="NEXT")

    # Notas
    pdf.add_page()
    pdf.add_notes([
        "Los estados financieros han sido preparados de acuerdo con las Normas Internacionales de Informacion Financiera (NIIF) emitidas por el IASB.",
        "El efectivo y equivalentes de efectivo incluyen depositos a plazo con vencimiento menor a 90 dias en BCP, BBVA y Scotiabank.",
        "Las cuentas por cobrar comerciales incluyen facturas por servicios de consultoria a organismos multilaterales (BID, Banco Mundial, CAF) con plazo promedio de cobro de 45 dias.",
        "Las inversiones en subsidiarias corresponden a participacion del 99.9% en Macro Wealth Management S.A. (MWM), Macro Kapital S.A.F.I. (MK) y Macro Invest S.A. (MIMA).",
        "Las obligaciones financieras de largo plazo corresponden a un prestamo sindicado con BCP a tasa SOFR + 2.5%, con vencimiento en 2028.",
        "La reserva legal se incremento en S/ 500 mil conforme a la Ley General de Sociedades (10% de la utilidad neta hasta alcanzar 20% del capital).",
        "Los gastos por derecho de uso corresponden al arrendamiento de oficinas en San Isidro, Lima (contrato hasta 2027).",
        "No existen contingencias legales significativas al cierre del periodo.",
    ])

    path = os.path.join(OUTPUT_DIR, "balance_general_macroconsult_2024.pdf")
    pdf.output(path)
    print(f"  ✓ {path} ({os.path.getsize(path):,} bytes)")
    return path


def generate_estado_resultados():
    pdf = EEFFReport()
    pdf.company_name = "MACROCAPITALES S.A.F.I."
    pdf.ruc = "20501234567"
    pdf.alias_nb_pages()
    pdf.add_page()

    pdf.add_title(
        "ESTADO DE RESULTADOS INTEGRALES",
        "Por los anos terminados el 31 de diciembre de 2024 y 2023\n(En miles de Soles)"
    )

    headers = ["Concepto", "2024", "2023", "Var %"]
    w = [pdf.epw * 0.45, pdf.epw * 0.18, pdf.epw * 0.18, pdf.epw * 0.19]

    ingresos = [
        ("Ingresos por comisiones de administracion", 18450, 15320, "20.4%"),
        ("Ingresos por comisiones de exito", 4200, 2800, "50.0%"),
        ("Ingresos por asesoria financiera", 3150, 2670, "18.0%"),
        ("Otros ingresos operacionales", 890, 720, "23.6%"),
        ("TOTAL INGRESOS OPERACIONALES", 26690, 21510, "24.1%"),
    ]
    rows = [(r[0], fmt(r[1]), fmt(r[2]), r[3]) for r in ingresos]
    pdf.add_section("Ingresos Operacionales")
    pdf.add_table(headers, rows, w)

    gastos = [
        ("Gastos de personal", -9870, -8540, "15.6%"),
        ("Servicios prestados por terceros", -3420, -2890, "18.3%"),
        ("Depreciacion y amortizacion", -1560, -1340, "16.4%"),
        ("Gastos de tecnologia e informacion", -2100, -1680, "25.0%"),
        ("Otros gastos operacionales", -1230, -980, "25.5%"),
        ("TOTAL GASTOS OPERACIONALES", -18180, -15430, "17.8%"),
    ]
    rows = [(r[0], fmt(r[1]), fmt(r[2]), r[3]) for r in gastos]
    pdf.add_section("Gastos Operacionales")
    pdf.add_table(headers, rows, w)

    resultado = [
        ("RESULTADO OPERACIONAL", 8510, 6080, "40.0%"),
        ("Ingresos financieros", 1230, 890, "38.2%"),
        ("Gastos financieros", -1870, -2100, "-11.0%"),
        ("Diferencia de cambio neta", -340, -180, "88.9%"),
        ("RESULTADO ANTES DE IMPUESTOS", 7530, 4690, "60.6%"),
        ("Impuesto a la renta (29.5%)", -2221, -1384, "60.5%"),
        ("RESULTADO NETO DEL EJERCICIO", 5309, 3306, "60.6%"),
    ]
    rows = [(r[0], fmt(r[1]), fmt(r[2]), r[3]) for r in resultado]
    pdf.add_section("Resultado del Ejercicio")
    pdf.add_table(headers, rows, w)

    # Indicadores
    pdf.add_page()
    pdf.add_section("Indicadores Financieros Clave")
    headers2 = ["Indicador", "2024", "2023"]
    w2 = [pdf.epw * 0.5, pdf.epw * 0.25, pdf.epw * 0.25]
    indicadores = [
        ("Margen operacional", "31.9%", "28.3%"),
        ("Margen neto", "19.9%", "15.4%"),
        ("ROE", "22.8%", "17.5%"),
        ("ROA", "12.1%", "9.2%"),
        ("Ratio de eficiencia (gastos/ingresos)", "68.1%", "71.7%"),
        ("AUM (activos bajo administracion, MM S/)", "2,450", "1,980"),
        ("Numero de fondos administrados", "5", "4"),
        ("Ticket promedio por cliente (miles S/)", "850", "720"),
    ]
    pdf.add_table(headers2, indicadores, w2)

    pdf.add_notes([
        "Las comisiones de administracion se calculan como porcentaje del valor cuota de cada fondo, conforme a los reglamentos de participacion aprobados por la SMV.",
        "Las comisiones de exito se reconocen al superar el benchmark establecido (IGBVL + 200bps para fondos de renta variable).",
        "Los gastos de tecnologia incluyen la implementacion del nuevo sistema de gestion de portafolios (Bloomberg AIM) por S/ 680 mil.",
        "La diferencia de cambio neta se origina por posiciones en USD de los fondos offshore (Macro Latam Fund - Islas Caiman).",
        "El impuesto a la renta se calcula a la tasa vigente del 29.5% conforme a la LIR peruana.",
        "Los fondos administrados por MK estan sujetos a supervision de la SMV y reportes trimestrales obligatorios.",
    ])

    path = os.path.join(OUTPUT_DIR, "estado_resultados_macrocapitales_2024.pdf")
    pdf.output(path)
    print(f"  ✓ {path} ({os.path.getsize(path):,} bytes)")
    return path


def generate_flujo_caja():
    pdf = EEFFReport()
    pdf.company_name = "MACRO INVEST S.A. (MIMA)"
    pdf.ruc = "20601234567"
    pdf.alias_nb_pages()
    pdf.add_page()

    pdf.add_title(
        "ESTADO DE FLUJOS DE EFECTIVO",
        "Por el ano terminado el 31 de diciembre de 2024\n(Metodo directo - En miles de Soles)"
    )

    headers = ["Concepto", "2024", "2023"]
    w = [pdf.epw * 0.55, pdf.epw * 0.22, pdf.epw * 0.23]

    # Operaciones
    pdf.add_section("Actividades de Operacion")
    operacion = [
        ("Cobros por servicios de intermediacion", 14200, 11800),
        ("Cobros por comisiones de estructuracion", 5600, 3900),
        ("Pagos a proveedores y personal", -12300, -10500),
        ("Pago de impuesto a la renta", -1850, -1230),
        ("Otros cobros (pagos) de operacion", -420, -310),
        ("FLUJO NETO DE OPERACION", 5230, 3660),
    ]
    rows = [(r[0], fmt(r[1]), fmt(r[2])) for r in operacion]
    pdf.add_table(headers, rows, w)

    # Inversion
    pdf.add_section("Actividades de Inversion")
    inversion = [
        ("Adquisicion de equipos de computo", -890, -540),
        ("Adquisicion de licencias software", -1200, -680),
        ("Inversion en plataforma digital", -2300, -1500),
        ("Venta de equipos obsoletos", 120, 80),
        ("FLUJO NETO DE INVERSION", -4270, -2640),
    ]
    rows = [(r[0], fmt(r[1]), fmt(r[2])) for r in inversion]
    pdf.add_table(headers, rows, w)

    # Financiamiento
    pdf.add_section("Actividades de Financiamiento")
    financiamiento = [
        ("Obtencion de prestamos bancarios", 3000, 5000),
        ("Amortizacion de prestamos", -2800, -2500),
        ("Pago de dividendos", -1500, -1000),
        ("Pago de arrendamientos (NIIF 16)", -780, -720),
        ("FLUJO NETO DE FINANCIAMIENTO", -2080, 780),
    ]
    rows = [(r[0], fmt(r[1]), fmt(r[2])) for r in financiamiento]
    pdf.add_table(headers, rows, w)

    pdf.ln(5)
    pdf.set_font("Helvetica", "B", 10)
    resumen = [
        ("Variacion neta del efectivo", -1120, 1800),
        ("Efectivo al inicio del periodo", 6340, 4540),
        ("Efectivo al cierre del periodo", 5220, 6340),
    ]
    for label, v24, v23 in resumen:
        pdf.cell(pdf.epw * 0.55, 7, label, border=1)
        pdf.cell(pdf.epw * 0.22, 7, fmt(v24), border=1, align="R")
        pdf.cell(pdf.epw * 0.23, 7, fmt(v23), border=1, align="R")
        pdf.ln()

    pdf.add_notes([
        "El estado de flujos de efectivo ha sido preparado bajo el metodo directo conforme a la NIC 7.",
        "La inversion en plataforma digital corresponde al desarrollo del sistema de negociacion electronica de renta fija (go-live Q2 2025).",
        "Los dividendos pagados corresponden a la distribucion aprobada en Junta General de Accionistas del 28 de marzo de 2024.",
        "El pago de arrendamientos financieros corresponde a las oficinas principales en Av. El Derby 254, Santiago de Surco.",
        "MIMA actua como sociedad agente de bolsa registrada ante la SMV con licencia vigente desde 2005.",
    ])

    path = os.path.join(OUTPUT_DIR, "flujo_caja_macroinvest_2024.pdf")
    pdf.output(path)
    print(f"  ✓ {path} ({os.path.getsize(path):,} bytes)")
    return path


if __name__ == "__main__":
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print("Generando PDFs de EEFF realistas para S4-OCR...")
    generate_balance_general()
    generate_estado_resultados()
    generate_flujo_caja()
    print("\n✓ Listo - 3 PDFs generados en", OUTPUT_DIR)
