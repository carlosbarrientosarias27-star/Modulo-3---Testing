"""
PARTE 5 — Tests para calcular_salario_neto(salario_bruto, horas_extra, categoria)
Generados con el prompt profesional diseñado en la Parte 5.

Ejecutar con: pytest tests/test_salario.py -v
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import pytest
from Intermedio.src.salario import calcular_salario_neto


# ─────────────────────────────────────────────
# CASOS NORMALES — Happy path por categoría
# ─────────────────────────────────────────────

class TestSalarioNormal:

    def test_junior_sin_horas_extra(self):
        """N1: Junior, 1500€ bruto, 0 horas extra → IRPF 15% → neto 1275€."""
        # Arrange
        salario_bruto = 1500.0
        horas_extra = 0
        categoria = "junior"
        # Act
        resultado = calcular_salario_neto(salario_bruto, horas_extra, categoria)
        # Assert
        assert resultado == 1275.0   # 1500 - 225 (15%) + 0

    def test_senior_con_horas_extra(self):
        """N2: Senior, 2500€ bruto, 5 horas extra → IRPF 22% + 75€ horas."""
        resultado = calcular_salario_neto(2500.0, 5, "senior")
        # 2500 - 550 + 75 = 2025
        assert resultado == 2025.0

    def test_manager_sin_horas_extra(self):
        """N3: Manager, 4000€ bruto, 0 horas extra → IRPF 30%."""
        resultado = calcular_salario_neto(4000.0, 0, "manager")
        # 4000 - 1200 = 2800
        assert resultado == 2800.0


# ─────────────────────────────────────────────
# CASOS LÍMITE — Valores en la frontera
# ─────────────────────────────────────────────

class TestSalarioLimite:

    def test_salario_minimo_positivo(self):
        """L1: Salario mínimo (0.01€) — válido aunque irreal."""
        resultado = calcular_salario_neto(0.01, 0, "junior")
        assert resultado > 0

    def test_muchas_horas_extra(self):
        """L2: 200 horas extra — horas extra > salario base es posible."""
        resultado = calcular_salario_neto(1000.0, 200, "junior")
        # 1000 - 150 + 3000 = 3850
        assert resultado == 3850.0

    def test_categoria_mayusculas(self):
        """L3: Categoría en mayúsculas ('SENIOR') — debe normalizarse."""
        resultado = calcular_salario_neto(2000.0, 0, "SENIOR")
        assert resultado == pytest.approx(1560.0)  # 2000 - 440


# ─────────────────────────────────────────────
# CASOS DE ERROR — Entradas inválidas
# ─────────────────────────────────────────────

class TestSalarioError:

    def test_salario_cero_lanza_error(self):
        """E1: Salario bruto = 0 — debe lanzar ValueError."""
        with pytest.raises(ValueError, match="positivo"):
            calcular_salario_neto(0.0, 0, "junior")

    def test_salario_negativo_lanza_error(self):
        """E2: Salario bruto negativo — debe lanzar ValueError."""
        with pytest.raises(ValueError, match="positivo"):
            calcular_salario_neto(-500.0, 0, "senior")

    def test_horas_extra_negativas_lanza_error(self):
        """E3: Horas extra negativas — debe lanzar ValueError."""
        with pytest.raises(ValueError, match="negativas"):
            calcular_salario_neto(2000.0, -3, "junior")

    def test_categoria_invalida_lanza_error(self):
        """E4: Categoría desconocida — debe lanzar ValueError."""
        with pytest.raises(ValueError, match="Categoría desconocida"):
            calcular_salario_neto(2000.0, 0, "becario")

    def test_tipo_salario_string_lanza_error(self):
        """E5: Salario como string — debe lanzar TypeError."""
        with pytest.raises(TypeError):
            calcular_salario_neto("dos mil", 0, "junior")

    def test_horas_extra_float_lanza_error(self):
        """E6: horas_extra como float — debe lanzar TypeError (debe ser int)."""
        with pytest.raises(TypeError):
            calcular_salario_neto(2000.0, 2.5, "junior")