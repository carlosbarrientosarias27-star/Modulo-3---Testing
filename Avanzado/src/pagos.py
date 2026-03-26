import stripe # Librería externa (se queda igual)
from src import db_module as db        # Cambiado: Importación relativa
from src import email_module as email  # Cambiado: Importación relativa

class PaymentError(Exception):
    pass

def procesar_pago(importe: float, tarjeta_id: str, usuario_id: int) -> dict:
    resultado = stripe.charge(importe, tarjeta_id)
    db.guardar_transaccion(usuario_id, resultado)
    email.enviar_confirmacion(usuario_id, importe)
    return {"status": "ok", "transaction_id": resultado["id"]}