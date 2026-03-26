"""
MÓDULO: descuento.py
Función calcular_descuento usada en PARTE 4 y retos opcionales.
"""


def calcular_descuento(precio: float, porcentaje: float) -> float:
    """
    Calcula el precio final tras aplicar un descuento.

    Args:
        precio: Precio original del producto (debe ser positivo).
        porcentaje: Porcentaje de descuento a aplicar (0-100).

    Returns:
        Precio final después del descuento.

    Raises:
        ValueError: Si precio o porcentaje son inválidos.
        TypeError: Si los tipos de entrada no son numéricos.
    """
    if not isinstance(precio, (int, float)) or not isinstance(porcentaje, (int, float)):
        raise TypeError("precio y porcentaje deben ser numéricos")
    if precio < 0:
        raise ValueError("El precio no puede ser negativo")
    if not (0 <= porcentaje <= 100):
        raise ValueError("El porcentaje debe estar entre 0 y 100")

    descuento = precio * (porcentaje / 100)
    return round(precio - descuento, 2)