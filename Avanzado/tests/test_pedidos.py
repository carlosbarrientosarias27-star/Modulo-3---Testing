"""
Tests unitarios para el módulo de pedidos de la tienda online.
Framework: pytest
Estructura: AAA (Arrange - Act - Assert)
Incluye: tests normales, de límite, de error y tests parametrizados.
"""

import pytest
from src.pedidos import aplicar_descuento, calcular_envio


# ============================================================
#  TESTS PARA aplicar_descuento
# ============================================================

class TestAplicarDescuento:

    # ---- Casos NORMALES ----

    def test_descuento_normal_cliente_estandar(self):
        # Arrange
        precio, porcentaje = 100.0, 10.0
        # Act
        resultado = aplicar_descuento(precio, porcentaje)
        # Assert
        assert resultado == 90.0

    def test_descuento_con_cliente_premium(self):
        # Arrange
        precio, porcentaje = 100.0, 10.0
        # Act
        resultado = aplicar_descuento(precio, porcentaje, cliente_premium=True)
        # Assert
        # 10% + 5% premium = 15% → 100 * 0.85 = 85.0
        assert resultado == 85.0

    def test_sin_descuento_porcentaje_cero(self):
        # Arrange
        precio = 50.0
        # Act
        resultado = aplicar_descuento(precio, 0.0)
        # Assert
        assert resultado == 50.0

    def test_redondeo_a_dos_decimales(self):
        # Arrange
        precio, porcentaje = 10.0, 3.0
        # Act
        resultado = aplicar_descuento(precio, porcentaje)
        # Assert
        assert resultado == 9.70

    # ---- Casos LÍMITE ----

    def test_precio_minimo_valido(self):
        # Arrange: precio justo por encima de 0
        resultado = aplicar_descuento(0.01, 0.0)
        assert resultado == 0.01

    def test_porcentaje_100_descuento_total(self):
        # Arrange
        resultado = aplicar_descuento(200.0, 100.0)
        # Assert: precio final debe ser 0
        assert resultado == 0.0

    def test_porcentaje_0_sin_descuento(self):
        resultado = aplicar_descuento(99.99, 0.0)
        assert resultado == 99.99

    def test_premium_con_porcentaje_96_clampeado_a_100(self):
        # Arrange: 96% + 5% premium = 101% → debe clampear a 100%
        resultado = aplicar_descuento(100.0, 96.0, cliente_premium=True)
        assert resultado == 0.0

    def test_porcentaje_exactamente_100_estandar(self):
        resultado = aplicar_descuento(500.0, 100.0)
        assert resultado == 0.0

    # ---- Casos de ERROR ----

    def test_precio_cero_lanza_valueerror(self):
        with pytest.raises(ValueError, match="precio"):
            aplicar_descuento(0.0, 10.0)

    def test_precio_negativo_lanza_valueerror(self):
        with pytest.raises(ValueError):
            aplicar_descuento(-50.0, 10.0)

    def test_porcentaje_negativo_lanza_valueerror(self):
        with pytest.raises(ValueError):
            aplicar_descuento(100.0, -5.0)

    def test_porcentaje_mayor_100_lanza_valueerror(self):
        with pytest.raises(ValueError):
            aplicar_descuento(100.0, 101.0)

    # ---- CASOS EDGE AÑADIDOS MANUALMENTE (no generados por IA) ----

    def test_precio_float_muy_pequeño_sin_descuento(self):
        """
        EDGE CASE PROPIO #1:
        Un precio de 0.001€ (fracción de céntimo) con 0% de descuento.
        La IA no lo generó porque trabajó con precios 'razonables'.
        Es importante porque sistemas con micropagos o criptomonedas pueden
        manejar valores muy pequeños y el redondeo podría distorsionar el resultado.
        """
        resultado = aplicar_descuento(0.001, 0.0)
        assert resultado == 0.0   # round(0.001, 2) == 0.0

    def test_descuento_premium_exactamente_95_porciento(self):
        """
        EDGE CASE PROPIO #2:
        Cliente premium con 95% de descuento → 95 + 5 = 100% exacto.
        La IA no probó la frontera exacta del clampeo para premium.
        Es importante verificar que el clampeo no genera precios negativos
        ni errores de redondeo en el límite exacto.
        """
        resultado = aplicar_descuento(1000.0, 95.0, cliente_premium=True)
        assert resultado == 0.0


# ---- Tests PARAMETRIZADOS para aplicar_descuento ----

@pytest.mark.parametrize("precio,porcentaje,premium,esperado", [
    (100.0,  10.0, False,  90.0),
    (200.0,  50.0, False, 100.0),
    (100.0,  10.0, True,   85.0),   # 10 + 5 = 15%
    (100.0,   0.0, False, 100.0),
    (100.0, 100.0, False,   0.0),
    ( 50.0,  20.0, False,  40.0),
    ( 99.99, 10.0, False,  89.99),
    (100.0,  95.0, True,    0.0),   # 95+5=100%, clamp
])
def test_aplicar_descuento_parametrizado(precio, porcentaje, premium, esperado):
    """
    Tests parametrizados que cubren múltiples combinaciones de precio,
    porcentaje y tipo de cliente en una sola función.
    Ventaja: evita duplicar código de test y hace evidente la tabla de casos.
    """
    resultado = aplicar_descuento(precio, porcentaje, premium)
    assert resultado == esperado


# ============================================================
#  TESTS PARA calcular_envio
# ============================================================

class TestCalcularEnvio:

    # ---- Casos NORMALES ----

    def test_envio_estandar_basico(self):
        # Arrange: 1 kg, 100 km, sin express
        # Act
        resultado = calcular_envio(1.0, 100)
        # Assert: 2.50 + 0.10 + 5.00 = 7.60
        assert resultado == 7.60

    def test_envio_express_aplica_recargo_50_porciento(self):
        # Arrange: 1 kg, 100 km, express
        resultado = calcular_envio(1.0, 100, express=True)
        # 7.60 * 1.50 = 11.40
        assert resultado == 11.40

    def test_envio_gratuito_peso_bajo_distancia_corta(self):
        # Arrange: 0.3 kg < 0.5 y 30 km < 50 → gratis
        resultado = calcular_envio(0.3, 30)
        assert resultado == 0.0

    def test_envio_gratuito_no_aplica_express_tambien_gratis(self):
        # Si el paquete cumple condición gratis, express no debería cobrar
        # (la lógica actual devuelve 0.0 antes de aplicar express)
        resultado = calcular_envio(0.3, 30, express=True)
        assert resultado == 0.0

    # ---- Casos LÍMITE ----

    def test_peso_exactamente_0_5_no_es_gratis(self):
        # peso == 0.5 NO es < 0.5 → debe pagar
        resultado = calcular_envio(0.5, 30)
        # 2.50 + 0.05 + 1.50 = 4.05
        assert resultado == 4.05

    def test_distancia_exactamente_50_no_es_gratis(self):
        # distancia == 50 NO es < 50 → debe pagar
        resultado = calcular_envio(0.3, 50)
        # 2.50 + 0.03 + 2.50 = 5.03
        assert resultado == 5.03

    def test_peso_justo_por_debajo_de_0_5_con_distancia_49(self):
        # 0.49 < 0.5 y 49 < 50 → gratis
        resultado = calcular_envio(0.49, 49)
        assert resultado == 0.0

    # ---- Casos de ERROR ----

    def test_peso_cero_lanza_valueerror(self):
        with pytest.raises(ValueError, match="peso"):
            calcular_envio(0.0, 100)

    def test_peso_negativo_lanza_valueerror(self):
        with pytest.raises(ValueError):
            calcular_envio(-1.0, 100)

    def test_distancia_cero_lanza_valueerror(self):
        with pytest.raises(ValueError, match="distancia"):
            calcular_envio(1.0, 0)

    def test_distancia_negativa_lanza_valueerror(self):
        with pytest.raises(ValueError):
            calcular_envio(1.0, -10)

    # ---- CASOS EDGE AÑADIDOS MANUALMENTE ----
    # (Los mismos que se cuentan en el análisis 2.3)

    def test_peso_muy_grande_sin_express(self):
        """
        EDGE CASE PROPIO #3 (calcular_envio):
        Paquete de 1000 kg y 10000 km. La IA no probó valores extremos reales.
        Cubre posibles desbordamientos numéricos o errores de rendimiento
        al calcular envíos industriales o internacionales.
        """
        resultado = calcular_envio(1000.0, 10000)
        # 2.50 + 100.00 + 500.00 = 602.50
        assert resultado == 602.50

    def test_express_con_paquete_en_frontera_exacta_de_gratuidad(self):
        """
        EDGE CASE PROPIO #4 (calcular_envio):
        Peso=0.5 kg (frontera exacta) con express=True.
        La IA no combinó frontera de gratuidad + express simultáneamente.
        Es importante porque un bug podría devolver 0.0 cuando debería cobrar
        con recargo express.
        """
        resultado = calcular_envio(0.5, 30, express=True)
        # No es gratis (peso=0.5 no es < 0.5)
        # base: 2.50 + (0.5*0.10) + (30*0.05) = 2.50 + 0.05 + 1.50 = 4.05
        # express: 4.05 * 1.5 = 6.075 → round(6.075, 2) = 6.07 (bankers rounding)
        assert resultado == 6.07


# ---- Tests PARAMETRIZADOS para calcular_envio ----

@pytest.mark.parametrize("peso,distancia,express,esperado", [
    (0.3,   30,  False, 0.0),     # gratis
    (0.49,  49,  False, 0.0),     # gratis (frontera justo debajo)
    (0.5,   30,  False, 4.05),    # frontera peso, no gratis
    (0.3,   50,  False, 5.03),    # frontera distancia, no gratis
    (1.0,  100,  False, 7.60),    # normal estándar
    (1.0,  100,  True,  11.40),   # normal express
    (2.0,   20,  False, 3.70),    # 2.50+0.20+1.00=3.70
    (5.0,  200,  True,  19.50),   # (2.50+0.50+10.00)=13.00 * 1.5 = 19.50
])
def test_calcular_envio_parametrizado(peso, distancia, express, esperado):
    resultado = calcular_envio(peso, distancia, express)
    assert resultado == esperado