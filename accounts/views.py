from django.shortcuts import render, get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework import generics, status
from drf_yasg.utils import swagger_auto_schema

from .serializers import RegisterSerializer, AccountSerializer, EmailSerializer, PasswordResetSerializer
from .permissions import IsOwnerOrReadonly
from .utils import create_reset_url
from .tasks import send_password_reset_link


User = get_user_model()


class RegisterView(APIView):
    """
    Принимает почту, пароль, подтверждение пароля, имя и фамилию
    """
    @swagger_auto_schema(request_body=RegisterSerializer)
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response("Вы успешно зарегистрировались!", 201)


class ActivationView(APIView):
    def get(self, request, email, activation_code):
        user = User.objects.filter(email=email, activation_code=activation_code).first()
        if not user:
            return Response("Пользователь не найден")
        user.activation_code = ""
        user.is_active = True
        user.save()
        return Response("Активировано", 200)



class AccountViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().filter(is_staff=False, is_superuser=False)
    serializer_class = AccountSerializer
    permission_classes = [IsOwnerOrReadonly]


class AccountDetailView(APIView):
    def get(self, request, email):
        try:
            user = User.objects.get(email=email)
            serializer = AccountSerializer(instance=user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)


class PasswordResetView(generics.GenericAPIView):
    serializer_class = EmailSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.data["email"]
        user = User.objects.filter(email=email).first()
        if  not user:
            return Response("Пользователь не найден", 404)
        encoded_pk = urlsafe_base64_encode(force_bytes(user.pk))
        token = PasswordResetTokenGenerator().make_token(user)
        link = create_reset_url(encoded_pk, token)
        send_password_reset_link.delay(email, link)

        return Response(f"Ваша ссылка для изменения пароля {link}",
            200)


class PasswordResetCompleteView(generics.GenericAPIView):
    serializer_class = PasswordResetSerializer

    def patch(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data,
            context={"kwargs": kwargs}
        )
        serializer.is_valid(raise_exception=True)

        return Response("Ваш пароль успешно изменён", status=status.HTTP_200_OK)