"""
Tests de integración con mocks para procesar_pago().
Framework: pytest + unittest.mock
"""
import pytest
from unittest.mock import patch, MagicMock
from src.pagos import procesar_pago, PaymentError


class TestProcesarPago:

    @patch("pagos.stripe.charge")
    @patch("pagos.db.guardar_transaccion")
    @patch("pagos.email.enviar_confirmacion")
    def test_pago_exitoso_devuelve_status_ok(self, mock_email, mock_db, mock_stripe):
        mock_stripe.return_value = {"id": "txn_123", "status": "succeeded"}
        resultado = procesar_pago(50.0, "card_abc", 1)
        assert resultado == {"status": "ok", "transaction_id": "txn_123"}

    @patch("pagos.stripe.charge")
    @patch("pagos.db.guardar_transaccion")
    @patch("pagos.email.enviar_confirmacion")
    def test_pago_exitoso_llama_stripe_con_parametros_correctos(self, mock_email, mock_db, mock_stripe):
        mock_stripe.return_value = {"id": "txn_456", "status": "succeeded"}
        procesar_pago(99.99, "card_xyz", 7)
        mock_stripe.assert_called_once_with(99.99, "card_xyz")

    @patch("pagos.stripe.charge")
    @patch("pagos.db.guardar_transaccion")
    @patch("pagos.email.enviar_confirmacion")
    def test_pago_exitoso_guarda_en_db(self, mock_email, mock_db, mock_stripe):
        mock_stripe.return_value = {"id": "txn_789", "status": "succeeded"}
        procesar_pago(25.0, "card_111", 3)
        mock_db.assert_called_once_with(3, {"id": "txn_789", "status": "succeeded"})

    @patch("pagos.stripe.charge")
    @patch("pagos.db.guardar_transaccion")
    @patch("pagos.email.enviar_confirmacion")
    def test_pago_exitoso_envia_email(self, mock_email, mock_db, mock_stripe):
        mock_stripe.return_value = {"id": "txn_000", "status": "succeeded"}
        procesar_pago(10.0, "card_222", 5)
        mock_email.assert_called_once_with(5, 10.0)

    @patch("pagos.stripe.charge")
    @patch("pagos.db.guardar_transaccion")
    @patch("pagos.email.enviar_confirmacion")
    def test_tarjeta_rechazada_lanza_payment_error(self, mock_email, mock_db, mock_stripe):
        mock_stripe.side_effect = PaymentError("Card declined")
        with pytest.raises(PaymentError, match="Card declined"):
            procesar_pago(50.0, "card_declined", 1)

    @patch("pagos.stripe.charge")
    @patch("pagos.db.guardar_transaccion")
    @patch("pagos.email.enviar_confirmacion")
    def test_tarjeta_rechazada_no_guarda_en_db(self, mock_email, mock_db, mock_stripe):
        mock_stripe.side_effect = PaymentError("Card declined")
        with pytest.raises(PaymentError):
            procesar_pago(50.0, "card_declined", 1)
        mock_db.assert_not_called()

    @patch("pagos.stripe.charge")
    @patch("pagos.db.guardar_transaccion")
    @patch("pagos.email.enviar_confirmacion")
    def test_tarjeta_rechazada_no_envia_email(self, mock_email, mock_db, mock_stripe):
        mock_stripe.side_effect = PaymentError("Card declined")
        with pytest.raises(PaymentError):
            procesar_pago(50.0, "card_declined", 1)
        mock_email.assert_not_called()

    @patch("pagos.stripe.charge")
    @patch("pagos.db.guardar_transaccion")
    @patch("pagos.email.enviar_confirmacion")
    def test_error_de_red_se_propaga(self, mock_email, mock_db, mock_stripe):
        mock_stripe.side_effect = ConnectionError("Network timeout")
        with pytest.raises(ConnectionError):
            procesar_pago(50.0, "card_ok", 2)

    @patch("pagos.stripe.charge")
    @patch("pagos.db.guardar_transaccion")
    @patch("pagos.email.enviar_confirmacion")
    def test_error_de_red_no_afecta_db_ni_email(self, mock_email, mock_db, mock_stripe):
        mock_stripe.side_effect = ConnectionError("Network timeout")
        with pytest.raises(ConnectionError):
            procesar_pago(50.0, "card_ok", 2)
        mock_db.assert_not_called()
        mock_email.assert_not_called()

    @patch("pagos.stripe.charge")
    @patch("pagos.db.guardar_transaccion")
    @patch("pagos.email.enviar_confirmacion")
    def test_db_caida_lanza_excepcion(self, mock_email, mock_db, mock_stripe):
        mock_stripe.return_value = {"id": "txn_ok", "status": "succeeded"}
        mock_db.side_effect = RuntimeError("DB connection lost")
        with pytest.raises(RuntimeError, match="DB connection lost"):
            procesar_pago(50.0, "card_ok", 2)

    @patch("pagos.stripe.charge")
    @patch("pagos.db.guardar_transaccion")
    @patch("pagos.email.enviar_confirmacion")
    def test_db_caida_no_envia_email(self, mock_email, mock_db, mock_stripe):
        mock_stripe.return_value = {"id": "txn_ok", "status": "succeeded"}
        mock_db.side_effect = RuntimeError("DB connection lost")
        with pytest.raises(RuntimeError):
            procesar_pago(50.0, "card_ok", 2)
        mock_email.assert_not_called()

    # ---- CASOS EDGE PROPIOS ----

    @patch("pagos.stripe.charge")
    @patch("pagos.db.guardar_transaccion")
    @patch("pagos.email.enviar_confirmacion")
    def test_todas_las_dependencias_son_llamadas_exactamente_una_vez(
            self, mock_email, mock_db, mock_stripe):
        """EDGE PROPIO #5: Verifica que ningún servicio se llame 0 o 2+ veces."""
        mock_stripe.return_value = {"id": "txn_seq", "status": "succeeded"}
        procesar_pago(30.0, "card_seq", 9)
        assert mock_stripe.call_count == 1
        assert mock_db.call_count == 1
        assert mock_email.call_count == 1

    @patch("pagos.stripe.charge")
    @patch("pagos.db.guardar_transaccion")
    @patch("pagos.email.enviar_confirmacion")
    def test_importe_cero_aun_llama_a_stripe(self, mock_email, mock_db, mock_stripe):
        """EDGE PROPIO #6: importe=0 no está validado; documenta el comportamiento actual."""
        mock_stripe.return_value = {"id": "txn_zero", "status": "succeeded"}
        resultado = procesar_pago(0.0, "card_ok", 1)
        mock_stripe.assert_called_once_with(0.0, "card_ok")
        assert resultado["status"] == "ok"