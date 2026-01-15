from datetime import date, timedelta
from apps.inventario.models import Producto


def evaluar_vencimiento(fecha_vencimiento, dias_alerta=3):
    dias_restantes = (fecha_vencimiento - date.today()).days

    if dias_restantes < 0:
        return "vencido", dias_restantes

    if dias_restantes <= dias_alerta:
        return "por_vencer", dias_restantes

    return "vigente", dias_restantes


def productos_por_vencer(dias_alerta=3):
    productos = Producto.objects.exclude(horas_caducidad=None)

    resultado = []

    for producto in productos:
        fecha_vencimiento = (
            producto.created_at + timedelta(hours=producto.horas_caducidad)
        ).date()

        estado, dias_restantes = evaluar_vencimiento(
            fecha_vencimiento, dias_alerta
        )

        if estado != "vigente":
            resultado.append({
                "id": producto.id,
                "nombre": producto.nombre,
                "fecha_vencimiento": fecha_vencimiento,
                "estado": estado,
                "dias_restantes": dias_restantes,
            })

    return resultado
