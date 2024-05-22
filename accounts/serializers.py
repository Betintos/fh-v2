from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_decode
from rest_framework import serializers

from .tasks import send_activation_code


User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=4, required=True, write_only=True)
    password_confirm = serializers.CharField(
        min_length=4, required=True, write_only=True
    )

    class Meta:
        model = User
        fields = ["email", "password", "password_confirm", "first_name", "last_name", ]

    def validate(self, attrs):
        p1 = attrs.get("password")
        p2 = attrs.pop("password_confirm")

        if p1 != p2:
            raise serializers.ValidationError("Пароли не совпадают")
        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        send_activation_code.delay(user.email, user.activation_code)
        return user


class AccountSerializer(serializers.ModelSerializer):
    subs_count = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ["id", "email", "first_name", "last_name", "profile_picture", "subs_count", "is_active"]

    def get_subs_count(self, obj):
        return obj.subscribers.count()

    
class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField()

    class Meta:
        fields = ["email"]


class PasswordResetSerializer(serializers.Serializer):
    password = serializers.CharField(min_length=4, required=True, write_only=True)
    password_confirm = serializers.CharField(
        min_length=4, required=True, write_only=True
    )

    class Meta:
        fields = ["password", "password_confirm"]

    def validate(self, data):
        p1 = data.get("password")
        p2 = data.get("password_confirm")
        if p1 != p2:
            raise serializers.ValidationError("Пароли не совпадают")

        token = self.context.get("kwargs").get("token")
        encoded_pk = self.context.get("kwargs").get("encoded_pk")
        if not token or not encoded_pk:
            raise  serializers.ValidationError("Нет данных")
            
        pk = urlsafe_base64_decode(encoded_pk).decode()
        user = User.objects.get(pk=pk)

        if not PasswordResetTokenGenerator().check_token(user, token):
            raise serializers.ValidationError("Неверный токен для изменеия")

        user.set_password(p1)
        user.save()
        return data