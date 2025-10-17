from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from users.models import CustomUser
# from users.models import UserConfirmation Code as ConfirmationCode
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from services.confirmation_code import validate_confirmation_code


class SendCodeSerializer(serializers.Serializer):
    user_id = serializers.IntegerField(required=True)

class VerifyCodeSerializer(serializers.Serializer):
    user_id = serializers.IntegerField(required=True)
    code = serializers.CharField(max_length=6, required=True)

class UserBaseSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()


class AuthValidateSerializer(UserBaseSerializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True)


class RegisterValidateSerializer(UserBaseSerializer):
    phone_number = serializers.CharField()
    birthdate = serializers.DateField()

    def validate_email(self, email):
        if CustomUser.objects.filter(email=email).exists():
            raise ValidationError('Email уже существует!')
        return email

    def validate_phone_number(self, phone_number):
        if not phone_number.isdigit():
            raise ValidationError('Номер телефона должен содержать только цифры!')
        if len(phone_number) < 10:
            raise ValidationError('Номер телефона слишком короткий!')
        return phone_number


class ConfirmationSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    code = serializers.CharField(max_length=6)

    def validate(self, attrs):
        user_id = attrs.get('user_id')
        code = attrs.get('code')

        # Проверяем существует ли пользователь
        try:
            user = CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist:
            raise ValidationError('Пользователь не существует!')

        # Проверяем код через Redis
        if not validate_confirmation_code(user.id, code):
            raise ValidationError('Неверный или истекший код подтверждения!')

        return attrs

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["email"] = user.email
        token["birthdate"] = str(user.birthdate)
        return token
    
    def validate(self, attrs):
        data = super().validate(attrs)
        data['email'] = self.user.email
        data['birthdate'] = str(self.user.birthdate)
        return data

class OauthCodeSerializer(serializers.Serializer):
    code = serializers.CharField()