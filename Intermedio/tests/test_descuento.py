"""
PARTE 4 — Tests para calcular_descuento(precio, porcentaje)
Casos tipo N (Normal), L (Límite) y E (Error).

Ejecutar con: pytest tests/test_descuento.py -v
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import pytest
from Intermedio.src.descuento import calcular_descuento


# ─────────────────────────────────────────────
# CASOS NORMALES (N) — Happy path
# ─────────────────────────────────────────────

class TestCasosNormales:
    """Casos donde todo funciona correctamente (happy path)."""

    def test_descuento_10_porciento(self):
        """N1: Descuento estándar del 10% sobre precio habitual."""
        # Arrange
        precio = 100.0
        porcentaje = 10.0
        # Act
        resultado = calcular_descuento(precio, porcentaje)
        # Assert
        assert resultado == 90.0

    def test_descuento_50_porciento(self):
        """N2: Descuento del 50% — mitad del precio."""
        resultado = calcular_descuento(200.0, 50.0)
        assert resultado == 100.0

    def test_descuento_con_decimales(self):
        resultado = calcular_descuento(49.99, 20.0)
        assert resultado == pytest.approx(39.99, abs=0.01) # Allows a small margin


# ─────────────────────────────────────────────
# CASOS LÍMITE (L) — Valores en la frontera
# ─────────────────────────────────────────────

class TestCasosLimite:
    """Valores extremos o de frontera."""

    def test_descuento_cero_porciento(self):
        """L1: 0% de descuento — el precio no debe cambiar."""
        resultado = calcular_descuento(150.0, 0.0)
        assert resultado == 150.0

    def test_descuento_100_porciento(self):
        """L2: 100% de descuento — el resultado debe ser 0."""
        resultado = calcular_descuento(300.0, 100.0)
        assert resultado == 0.0

    def test_precio_muy_pequeno(self):
        """L3: Precio mínimo (0.01€) — funciona con valores casi cero."""
        resultado = calcular_descuento(0.01, 0.0)
        assert resultado == 0.01


# ─────────────────────────────────────────────
# CASOS DE ERROR (E) — Entradas inválidas
# ─────────────────────────────────────────────

class TestCasosError:
    """Entradas inválidas que deben provocar errores controlados."""

    def test_precio_negativo_lanza_error(self):
        """E1: Precio negativo — debe lanzar ValueError."""
        with pytest.raises(ValueError, match="negativo"):
            calcular_descuento(-50.0, 10.0)

    def test_porcentaje_mayor_100_lanza_error(self):
        """E2: Porcentaje mayor de 100 — debe lanzar ValueError."""
        with pytest.raises(ValueError, match="entre 0 y 100"):
            calcular_descuento(100.0, 110.0)

    def test_tipo_incorrecto_string_lanza_error(self):
        """E3: Precio como string — debe lanzar TypeError."""
        with pytest.raises(TypeError, match="numéricos"):
            calcular_descuento("cien", 10.0)