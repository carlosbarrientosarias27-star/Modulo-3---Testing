def aplicar_descuento(precio: float, porcentaje: float, cliente_premium: bool = False) -> float:
    """Aplica descuento al precio. Clientes premium tienen un 5% adicional.
    Lanza ValueError si precio <= 0 o porcentaje fuera de rango [0, 100].
    Devuelve el precio final redondeado a 2 decimales."""
    if precio <= 0:
        raise ValueError("El precio debe ser mayor que 0")
    if not (0 <= porcentaje <= 100):
        raise ValueError("El porcentaje debe estar entre 0 y 100")

    descuento_total = porcentaje
    if cliente_premium:
        descuento_total += 5
    # Clampear al máximo del 100%
    descuento_total = min(descuento_total, 100)

    precio_final = precio * (1 - descuento_total / 100)
    return round(precio_final, 2)


def calcular_envio(peso_kg: float, distancia_km: int, express: bool = False) -> float:
    """Calcula el coste de envío: base 2.50€ + 0.10€/kg + 0.05€/km.
    Envío express tiene recargo del 50%. Gratis si peso < 0.5kg y distancia < 50km.
    Lanza ValueError si peso <= 0 o distancia <= 0."""
    if peso_kg <= 0:
        raise ValueError("El peso debe ser mayor que 0")
    if distancia_km <= 0:
        raise ValueError("La distancia debe ser mayor que 0")

    # Envío gratuito para paquetes pequeños y cercanos
    if peso_kg < 0.5 and distancia_km < 50:
        return 0.0

    coste = 2.50 + (peso_kg * 0.10) + (distancia_km * 0.05)

    if express:
        coste *= 1.50

    return round(coste, 2)