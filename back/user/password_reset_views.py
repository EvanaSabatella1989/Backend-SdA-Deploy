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

    if not email:
        return Response(
            {"error": "El email es requerido"},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        # IMPORTANTE: no revelar si el email existe o no
        return Response(
            {"message": "Si el correo existe, se enviará un email"},
            status=status.HTTP_200_OK
        )

    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)

    reset_link = f"https://TU-FRONTEND/password-reset-confirm/{uid}/{token}/"
    reset_link = f"{settings.FRONTEND_URL}/password-reset-confirm/{uid}/{token}/"

    send_mail(
        subject="Recuperación de contraseña",
        message=f"Entrá al siguiente link para cambiar tu contraseña:\n{reset_link}",
        from_email="no-reply@tuapp.com",
        recipient_list=[user.email],
        fail_silently=False,
    )

    return Response(
        {"message": "Si el correo existe, se enviará un email"},
        status=status.HTTP_200_OK
    )

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
