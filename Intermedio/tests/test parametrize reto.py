"""
RETO OPCIONAL — Tests parametrizados con @pytest.mark.parametrize
para calcular_descuento. 5 combinaciones en un solo test.

Ventaja: un solo test cubre múltiples casos, sin duplicar código.
Si falla, pytest indica exactamente qué combinación falló.

Ejecutar con: pytest tests/test_parametrize_reto.py -v
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import pytest
from descuento import calcular_descuento


@pytest.mark.parametrize("precio, porcentaje, esperado", [
    (100.0,  10.0,  90.0),   # descuento básico 10%
    (200.0,  50.0, 100.0),   # mitad del precio
    (0.0,    25.0,   0.0),   # precio cero → siempre 0
    (99.99,   0.0,  99.99),  # sin descuento → precio igual
    (500.0, 100.0,   0.0),   # descuento total
])
def test_calcular_descuento_parametrizado(precio, porcentaje, esperado):
    """
    Test parametrizado: 5 combinaciones en un único test.
    Ventaja vs 5 tests separados:
    - Menos código, más fácil de mantener.
    - Añadir un caso nuevo = añadir una línea a la lista.
    - pytest muestra qué combinación falla de forma clara.
    """
    resultado = calcular_descuento(precio, porcentaje)
    assert resultado == esperado