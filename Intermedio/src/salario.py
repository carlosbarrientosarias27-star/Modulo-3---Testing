"""
MÓDULO: salario.py
Función calcular_salario_neto usada en PARTE 5.
"""

IRPF = {
    "junior": 0.15,
    "senior": 0.22,
    "manager": 0.30,
}

PAGO_HORA_EXTRA = 15.0


def calcular_salario_neto(salario_bruto: float, horas_extra: int, categoria: str) -> float:
    """
    Calcula el salario neto aplicando IRPF según categoría (junior/senior/manager),
    añadiendo el pago de horas extra (15€/hora) y validando que los valores sean positivos.

    Args:
        salario_bruto: Salario bruto mensual en euros (debe ser > 0).
        horas_extra: Número de horas extra realizadas (debe ser >= 0).
        categoria: Categoría del empleado ('junior', 'senior', 'manager').

    Returns:
        Salario neto calculado en euros.

    Raises:
        ValueError: Si algún valor es inválido (negativo o categoría desconocida).
        TypeError: Si los tipos de entrada son incorrectos.
    """
    if not isinstance(salario_bruto, (int, float)):
        raise TypeError("salario_bruto debe ser numérico")
    if not isinstance(horas_extra, int):
        raise TypeError("horas_extra debe ser un entero")
    if not isinstance(categoria, str):
        raise TypeError("categoria debe ser un string")

    if salario_bruto <= 0:
        raise ValueError("El salario bruto debe ser positivo")
    if horas_extra < 0:
        raise ValueError("Las horas extra no pueden ser negativas")

    categoria = categoria.lower().strip()
    if categoria not in IRPF:
        raise ValueError(f"Categoría desconocida: '{categoria}'. Use: junior, senior, manager")

    tipo_irpf = IRPF[categoria]
    importe_irpf = salario_bruto * tipo_irpf
    importe_horas_extra = horas_extra * PAGO_HORA_EXTRA

    salario_neto = salario_bruto - importe_irpf + importe_horas_extra
    return round(salario_neto, 2)