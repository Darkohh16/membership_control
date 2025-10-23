from datetime import datetime


def generar_numero_recibo():
    """
    Genera un número de recibo único basado en la fecha y hora actual.
    Formato: REC-YYYYMMDD-HHMMSS
    """
    now = datetime.now()
    return f"REC-{now.strftime('%Y%m%d-%H%M%S')}"


def calcular_descuento(monto, porcentaje_descuento=0):
    """
    Calcula el monto final después de aplicar un descuento.
    """
    if porcentaje_descuento > 0:
        descuento = monto * (porcentaje_descuento / 100)
        return monto - descuento
    return monto


def validar_monto(monto):
    """
    Valida que el monto sea válido (mayor a 0).
    """
    return monto > 0
