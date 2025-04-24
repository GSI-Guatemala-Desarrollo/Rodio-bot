# Caso solo IVA
def iva_gen_calcular_linea_1(total1, retencion_iva):
    total2 = total1 * 1.12
    iva1 = total2 - total1
    iva2 = iva1 * retencion_iva

    return {
        "IVA2": iva2
    }

# Caso PEQ Contribuyente
def iva_peq_calcular_linea_1(total1, retencion_iva):
    total2 = total1 * 1.12
    iva2 = total2 * retencion_iva

    return {
        "IVA2": iva2
    }


# Caso 1. IVA - ISR > 30K
def caso1_calcular_linea_1(base, total1, retencion_isr, retencion_iva):
    """Calcula los valores para la línea 1."""
    l1total2 = total1 * 1.12
    l1total3 = base * 1.12
    iva1 = base * 0.12
    isr = base * retencion_isr
    iva2 = iva1 * retencion_iva

    return {
        "L1TOTAL2": l1total2,
        "L1TOTAL3": l1total3,
        "IVA1": iva1,
        "ISR": isr,
        "IVA2": iva2
    }


def caso1_calcular_linea_2(total1, l1total2, l1total3, retencion_isr, retencion_iva):
    """Calcula los valores para la línea 2."""
    total2 = total1 * 1.12
    total3 = total2 - (l1total3 - l1total2)
    base = total3 / 1.12
    iva1 = base * 0.12
    isr = base * retencion_isr
    iva2 = iva1 * retencion_iva

    return {
        "TOTAL2": total2,
        "TOTAL3": total3,
        "BASE": base,
        "IVA1": iva1,
        "ISR": isr,
        "IVA2": iva2
    }


def caso1_calcular_linea_3(total1, retencion_isr, retencion_iva):
    """Calcula los valores para las líneas 3 (pueden ser varias)."""
    total2 = total1 * 1.12
    total3 = total2
    base = total3 / 1.12
    iva1 = base * 0.12
    isr = base * retencion_isr
    iva2 = iva1 * retencion_iva

    return {
        "TOTAL2": total2,
        "TOTAL3": total3,
        "BASE": base,
        "IVA1": iva1,
        "ISR": isr,
        "IVA2": iva2
    }

# Caso 2. IVA - ISR < 30K
def caso2_calcular_linea_1(total1, retencion_isr, retencion_iva):
    """Calcula los valores para la línea 1 del caso 2."""
    total2 = total1 * 1.12
    iva1 = total2 - total1
    isr = total1 * retencion_isr
    iva2 = iva1 * retencion_iva

    return {
        "TOTAL2": total2,
        "IVA1": iva1,
        "ISR": isr,
        "IVA2": iva2
    }


def caso2_calcular_linea_2(total1, base, retencion_isr, retencion_iva):
    """Calcula los valores para la línea 2 del caso 2."""
    total2 = total1 * 1.12
    iva1 = total2 - total1
    isr = base * retencion_isr
    iva2 = iva1 * retencion_iva

    return {
        "TOTAL2": total2,
        "IVA1": iva1,
        "ISR": isr,
        "IVA2": iva2
    }


# Caso IVA - ISR < 30K 1 Linea OC
def caso5_calcular_linea_1(base, total1, retencion_isr, retencion_iva):
    """Calcula los valores para la línea 1 del caso 5."""
    l1total2 = total1 * 1.12
    l1total3 = base * 1.12
    iva1 = base * 0.12
    isr = base * retencion_isr
    iva2 = iva1 * retencion_iva

    return {
        "L1TOTAL2": l1total2,
        "L1TOTAL3": l1total3,
        "IVA1": iva1,
        "ISR": isr,
        "IVA2": iva2
    }


def caso5_calcular_linea_2(total1, l1total2, l1total3, retencion_isr, retencion_iva):
    """Calcula los valores para la línea 2 del caso 5."""
    total2 = total1 * 1.12
    total3 = total2 - (l1total3 - l1total2)
    base = total3 / 1.12
    iva1 = base * 0.12
    isr = base * retencion_isr
    iva2 = iva1 * retencion_iva

    return {
        "TOTAL2": total2,
        "TOTAL3": total3,
        "BASE": base,
        "IVA1": iva1,
        "ISR": isr,
        "IVA2": iva2
    }
