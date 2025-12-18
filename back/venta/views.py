# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# import requests
# from carrito.models import Carrito, CarritoItem
# from venta.models import Venta
# from venta_detalle.models import VentaDetalle
# from user.models import Cliente  # Asegúrate de que el usuario tiene un cliente asociado
# from decimal import Decimal
# from django.db import transaction
# # Create your views here.
# # SDK de Mercado Pago
# import mercadopago
# # Agrega credenciales
# sdk = mercadopago.SDK("APP_USR-4989301092010028-031112-8ec03be037cc76704baaec21a1604e49-2319025513")


# class ReferenceMPView(APIView):
#     def post(self, request, format=None):
#         user = request.user  # Usuario autenticado
#         carrito = Carrito.objects.get(user=user)
#         items = request.data.get("items")
#         newlist = [
#             {
#             "unit_price": float(x.pop("precio")),
#             "title": x.pop("nombre"),
#             "quantity": x.pop("cantidad"),
#             **x
#             }
#              if "precio" and "cantidad" and "nombre" in x else x for x in items]
#         infoClient = request.data.get("client")
#        # Crea un ítem en la preferencia
#         if items:
#             preference_data = {
#                 "items": newlist,
#                 "back_urls": {  # ✅ Agregar URLs de retorno
#                     "success": "http://localhost:4200/pago-exitoso",
#                     "failure": "http://localhost:4200/pago-fallido",
#                     "pending": "http://localhost:4200/pago-pendiente"
#                 },
#                 "auto_return": "approved"  # ✅ Redirección automática cuando el pago sea aprobado
#             }

#             preference = sdk.preference().create(preference_data)
#             print(preference)
#             if preference['status'] == 400:

#                 return Response(status=status.HTTP_404_NOT_FOUND)
#             response = preference["response"]
#             print(response)
#             # return Response({"init_point": response["init_point"]})
#             return Response({"init_point": response.get("init_point", "No disponible")})
#         return Response(status=status.HTTP_404_NOT_FOUND)


# class ConfirmarPagoView(APIView):
#     def post(self, request, format=None):
#         """
#         Confirma el pago exitoso, guarda la venta en la BD y vacía el carrito.
#         """
#         user = request.user  # Usuario autenticado
#         pago_status = request.data.get("status")  # Estado del pago recibido
#         payment_id = request.data.get("payment_id")  # ID del pago en Mercado Pago

#         if pago_status != "approved":
#             return Response({"error": "El pago no fue aprobado"}, status=status.HTTP_400_BAD_REQUEST)

#         try:
#             carrito = Carrito.objects.get(user=user)
#             cliente = Cliente.objects.get(user=user)  # Obtener el cliente desde el usuario
#             total_venta = sum(item.producto.precio * item.cantidad for item in carrito.items.all())

#             with transaction.atomic():  # Garantizar que todas las operaciones sean atómicas
#                 # Crear la venta
#                 venta = Venta.objects.create(
#                     numero_factura=payment_id,  # Usamos el payment_id como referencia
#                     total=Decimal(total_venta),
#                     tipo_pago="tarjeta",
#                     estado="completada",
#                     cliente=cliente
#                 )

#                 # Guardar detalles de venta
#                 for item in carrito.items.all():
#                     VentaDetalle.objects.create(
#                         venta=venta,
#                         producto=item.producto,
#                         cantidad=item.cantidad,
#                         precio=item.producto.precio,
#                         descuento=Decimal(0)  # Si no hay descuento, puede ser 0
#                     )

#                 # Vaciar el carrito eliminando los items
#                 carrito.items.all().delete()

#             return Response({"message": "Venta registrada y carrito vaciado con éxito"}, status=status.HTTP_200_OK)

#         except Carrito.DoesNotExist:
#             return Response({"error": "Carrito no encontrado"}, status=status.HTTP_404_NOT_FOUND)
#         except Cliente.DoesNotExist:
#             return Response({"error": "Cliente no encontrado"}, status=status.HTTP_404_NOT_FOUND)
#         except Exception as e:
#             return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)






from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import requests
from carrito.models import Carrito, CarritoItem
from venta.models import Venta
from venta_detalle.models import VentaDetalle
from user.models import Cliente  # Importar Cliente
from decimal import Decimal
from django.db import transaction
import mercadopago
from django.shortcuts import get_object_or_404
from django.conf import settings
from .serializer import VentaSerializer

# Agrega credenciales de Mercado Pago
sdk = mercadopago.SDK("APP_USR-4989301092010028-031112-8ec03be037cc76704baaec21a1604e49-2319025513")

# Función auxiliar para obtener el Cliente desde el usuario autenticado
def get_cliente_from_request(request):
    return get_object_or_404(Cliente, user=request.user)

class ReferenceMPView(APIView):
    def post(self, request, format=None):
        cliente = get_cliente_from_request(request)  # Obtener el Cliente asociado al usuario
        carrito = get_object_or_404(Carrito, user=cliente)  # Buscar el carrito del cliente
        items = request.data.get("items")

        if not items:
            return Response({"error": "No hay productos en el carrito"}, status=status.HTTP_400_BAD_REQUEST)

        newlist = [
            {
                "unit_price": float(x.pop("precio")),
                "title": x.pop("nombre"),
                "quantity": x.pop("cantidad"),
                **x
            }
            if "precio" in x and "cantidad" in x and "nombre" in x else x for x in items
        ]

        FRONTEND_URL = getattr(settings, "FRONTEND_URL", "http://localhost:4200")

        preference_data = {
            "items": newlist,
            "back_urls": {
                # "success": f"{FRONTEND_URL}/pago-exitoso",
                # "failure": f"{FRONTEND_URL}/pago-fallido",
                # "pending": f"{FRONTEND_URL}/pago-pendiente",
                "success": "https://evanasabatella1989.github.io/Frontend-SdA-Deploy/#/pago-exitoso",
                "failure": "https://evanasabatella1989.github.io/Frontend-SdA-Deploy/#/pago-fallido",
                "pending": "https://evanasabatella1989.github.io/Frontend-SdA-Deploy/#/pago-pendiente",
            },
            "auto_return": "approved"
        }

       


        preference = sdk.preference().create(preference_data)

        if preference['status'] == 400:
            print(preference)
            return Response({"error": "Error al crear la preferencia de pago"}, status=status.HTTP_400_BAD_REQUEST)

        response = preference.get("response", {})
        return Response({"init_point": response.get("init_point", "No disponible")}, status=status.HTTP_200_OK)


class ConfirmarPagoView(APIView):
    def post(self, request, format=None):
        """
        Confirma el pago exitoso, guarda la venta en la BD y vacía el carrito.
        """
        cliente = get_cliente_from_request(request)  # Obtener el Cliente asociado al usuario
        pago_status = request.data.get("status")  # Estado del pago recibido
        payment_id = request.data.get("payment_id")  # ID del pago en Mercado Pago

        
        if pago_status.lower() != "approved":
            return Response({"error": "El pago no fue aprobado"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            carrito = get_object_or_404(Carrito, user=cliente)  # Obtener el carrito del cliente
            total_venta = sum(item.producto.precio * item.cantidad for item in carrito.items.all())

            # Consultar pago en Mercado Pago
            payment_info = sdk.payment().get(payment_id)
            if payment_info['status'] != 200:
                return Response({"error": "No se pudo obtener la información del pago desde Mercado Pago"},
                                status=status.HTTP_400_BAD_REQUEST)

            payment_data = payment_info["response"]
            tipo_pago = payment_data.get("payment_type_id", "desconocido")
            estado = payment_data.get("status", "pendiente")

            with transaction.atomic():  # Garantizar que todas las operaciones sean atómicas
                # Crear la venta
                venta = Venta.objects.create(
                    numero_factura=payment_id,
                    total=Decimal(total_venta),
                    tipo_pago=tipo_pago,
                    estado="completada" if estado == "approved" else estado,
                    cliente=cliente
                )

                # Guardar detalles de venta
                for item in carrito.items.all():
                    producto = item.producto
                    cantidad_vendida = item.cantidad

                    # Crear el detalle de venta
                    VentaDetalle.objects.create(
                        venta=venta,
                        producto=producto,
                        cantidad=cantidad_vendida,
                        precio=producto.precio,
                        descuento=Decimal(0)
                    )

                    #  Descontar cantidad disponible del producto
                    if producto.cantidad >= cantidad_vendida:
                        producto.cantidad -= cantidad_vendida
                        producto.save()
                    else:
                        raise ValueError(f"Cantidad insuficiente para el producto {producto.nombre}")

                # Vaciar el carrito
                carrito.items.all().delete()

            return Response({"message": "Venta registrada, cantidad actualizada y carrito vaciado con éxito"},
                            status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class VentaListView(APIView):

    def get(self, request):
        ventas = Venta.objects.all().order_by('-fecha_pago')
        serializer = VentaSerializer(ventas, many=True)
        return Response(serializer.data)


class VentaDetailView(APIView):

    def get(self, request, pk):
        venta = get_object_or_404(Venta, pk=pk)
        serializer = VentaSerializer(venta)
        return Response(serializer.data)

    def put(self, request, pk):
        venta = get_object_or_404(Venta, pk=pk)
        serializer = VentaSerializer(venta, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        venta = get_object_or_404(Venta, pk=pk)
        venta.delete()
        return Response(
            {"message": "Venta eliminada correctamente"},
            status=status.HTTP_204_NO_CONTENT
        )




# class ReferenceMPView(APIView):
#     def post(self, request, format=None):

#         ACCESS_TOKEN = "APP_USR-936168452210572-061619-f651358d6e63a47ac60b46fe256f4e2d-582661966"
#         url = "https://api.mercadopago.com/checkout/preferences"
#         headers = {
#             "Authorization": f"Bearer {ACCESS_TOKEN}",
#            "Accept": "application/json"
#         }

#         response = requests.get(url, headers=headers)

#         # Verificar si la respuesta es JSON antes de convertirla
#         if response.status_code == 200:
#          try:
#                print(response.json())  # Si la respuesta es válida, imprimir el JSON
#          except requests.exceptions.JSONDecodeError:
#                 print("La respuesta no es un JSON válido:", response.text)
#         else:
#             print(f"Error {response.status_code}: {response.text}")  # Ver mensaje de error






#         items = request.data.get("items")

#         if not items:
#             return Response({"error": "No se recibieron items"}, status=status.HTTP_400_BAD_REQUEST)

#         try:
#             newlist = [
#                 {"unit_price": float(x["precio"]), 
#                  "title": x["nombre"], 
#                  "quantity": x["cantidad"]} 
#                 for x in items if all(k in x for k in ["precio", "nombre", "cantidad"])
#             ]
#         except KeyError:
#             return Response({"error": "Formato de items incorrecto"}, status=status.HTTP_400_BAD_REQUEST)

#         preference_data = {"items": newlist}
#         print("Datos enviados a Mercado Pago:", preference_data)

#         preference = sdk.preference().create(preference_data)

#         if "error" in preference:
#             return Response({"error": "Error de Mercado Pago", "details": preference}, status=status.HTTP_400_BAD_REQUEST)

#         response = preference.get("response", {})

#         if "init_point" not in response:
#             return Response({"error": "No se pudo generar el enlace de pago", "details": response}, status=status.HTTP_400_BAD_REQUEST)

#         return Response({"init_point": response["init_point"]})
