import stripe
# El punto (.) significa "busca en esta misma carpeta (src)"
from . import db_module as db
from . import email_module as email

class PaymentError(Exception):
    pass

def procesar_pago(importe: float, tarjeta_id: str, usuario_id: int) -> dict:
    resultado = stripe.charge(importe, tarjeta_id)
    db.guardar_transaccion(usuario_id, resultado)
    email.enviar_confirmacion(usuario_id, importe)
    return {"status": "ok", "transaction_id": resultado["id"]}