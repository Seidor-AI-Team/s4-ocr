"""
validator.py — Validación de consistencia matemática entre campos extraídos
"""


def parse_number(value: str) -> float | None:
    """Intenta convertir un string a número."""
    try:
        clean = value.replace(",", "").replace("S/", "").replace("$", "").replace("%", "").strip()
        return float(clean)
    except (ValueError, AttributeError):
        return None


def validate_consistency(results: list) -> list:
    """
    Verifica reglas de consistencia financiera.
    Retorna lista de issues encontrados.
    """
    issues = []
    data = {r.field: r.value for r in results}

    def get_num(field_name: str) -> float | None:
        val = data.get(field_name)
        return parse_number(val) if val else None

    # Regla 1: Total Activos = Activos Corrientes + Activos No Corrientes
    total_activos = get_num("Total Activos")
    activos_corrientes = get_num("Activos Corrientes")
    activos_no_corrientes = get_num("Activos No Corrientes")

    if all(v is not None for v in [total_activos, activos_corrientes, activos_no_corrientes]):
        suma = activos_corrientes + activos_no_corrientes
        diff = abs(total_activos - suma)
        if diff > 1:  # tolerancia de 1 unidad
            issues.append({
                "rule": "Balance de Activos",
                "message": f"Total Activos ({total_activos:,.0f}) ≠ Corrientes + No Corrientes ({suma:,.0f})",
                "severity": "high",
                "fields": ["Total Activos", "Activos Corrientes", "Activos No Corrientes"]
            })

    # Regla 2: Total Activos = Total Pasivos + Patrimonio Neto
    total_pasivos = get_num("Total Pasivos")
    patrimonio = get_num("Patrimonio Neto")

    if all(v is not None for v in [total_activos, total_pasivos, patrimonio]):
        suma = total_pasivos + patrimonio
        diff = abs(total_activos - suma)
        if diff > 1:
            issues.append({
                "rule": "Ecuación Contable",
                "message": f"Activos ({total_activos:,.0f}) ≠ Pasivos + Patrimonio ({suma:,.0f})",
                "severity": "high",
                "fields": ["Total Activos", "Total Pasivos", "Patrimonio Neto"]
            })

    # Regla 3: Flujo de Caja — Saldo Final = Saldo Inicial + Flujo Neto
    saldo_inicial = get_num("Saldo Inicial")
    saldo_final = get_num("Saldo Final")
    flujo_neto = get_num("Flujo Neto Total")

    if all(v is not None for v in [saldo_inicial, saldo_final, flujo_neto]):
        esperado = saldo_inicial + flujo_neto
        diff = abs(saldo_final - esperado)
        if diff > 1:
            issues.append({
                "rule": "Cuadre de Caja",
                "message": f"Saldo Final ({saldo_final:,.0f}) ≠ Inicial + Flujo Neto ({esperado:,.0f})",
                "severity": "medium",
                "fields": ["Saldo Inicial", "Saldo Final", "Flujo Neto Total"]
            })

    # Regla 4: Utilidad Bruta = Ingresos - Costo de Ventas
    ingresos = get_num("Ingresos Totales")
    costo_ventas = get_num("Costo de Ventas")
    utilidad_bruta = get_num("Utilidad Bruta")

    if all(v is not None for v in [ingresos, costo_ventas, utilidad_bruta]):
        esperado = ingresos - costo_ventas
        diff = abs(utilidad_bruta - esperado)
        if diff > 1:
            issues.append({
                "rule": "Utilidad Bruta",
                "message": f"Utilidad Bruta ({utilidad_bruta:,.0f}) ≠ Ingresos - Costos ({esperado:,.0f})",
                "severity": "medium",
                "fields": ["Ingresos Totales", "Costo de Ventas", "Utilidad Bruta"]
            })

    return issues
