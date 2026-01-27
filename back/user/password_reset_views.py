from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import send_mail
from django.conf import settings
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status

User = get_user_model()


@api_view(['POST'])
@permission_classes([AllowAny])
def password_reset_request(request):
    email = request.data.get('email')

    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        # x seguridad, no decimos que no existe
        return Response({
            "message": "Si el usuario existe, se enviará el enlace"
        })

    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)

    reset_url = (
        "https://evanasabatella1989.github.io/Frontend-SdA-Deploy/"
        f"#/password-reset-confirm/{uid}/{token}"
    )

    return Response({
        "reset_url": reset_url
    })

@api_view(['POST'])
@permission_classes([AllowAny])
def password_reset_confirmar(request):
    uid = request.data.get('uid')
    token = request.data.get('token')
    new_password = request.data.get('new_password')

    if not uid or not token or not new_password:
        return Response(
            {"error": "Datos incompletos"},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        user_id = force_str(urlsafe_base64_decode(uid))
        user = User.objects.get(pk=user_id)
    except (User.DoesNotExist, ValueError, TypeError):
        return Response(
            {"error": "Token inválido"},
            status=status.HTTP_400_BAD_REQUEST
        )

    if not default_token_generator.check_token(user, token):
        return Response(
            {"error": "Token inválido o expirado"},
            status=status.HTTP_400_BAD_REQUEST
        )

    user.set_password(new_password)
    user.save()

    return Response(
        {"message": "Contraseña actualizada correctamente"},
        status=status.HTTP_200_OK
    )
