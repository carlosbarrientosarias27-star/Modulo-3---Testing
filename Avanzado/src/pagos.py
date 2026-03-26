import stripe_module as stripe
import db_module as db
import email_module as email


class PaymentError(Exception):
    pass


def procesar_pago(importe: float, tarjeta_id: str, usuario_id: int) -> dict:
    """Llama a stripe.charge() para cobrar, guarda en DB y envía email de confirmación.
    Devuelve {"status": "ok", "transaction_id": "..."} o lanza PaymentError."""
    resultado = stripe.charge(importe, tarjeta_id)
    db.guardar_transaccion(usuario_id, resultado)
    email.enviar_confirmacion(usuario_id, importe)
    return {"status": "ok", "transaction_id": resultado["id"]}