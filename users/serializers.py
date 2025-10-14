from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from users.models import CustomUser
from users.models import UserConfirmationCode as ConfirmationCode
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer



class UserBaseSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()


class AuthValidateSerializer(UserBaseSerializer):
    pass


class RegisterValidateSerializer(UserBaseSerializer):
    phone_number = serializers.CharField()

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

        try:
            user = CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist:
            raise ValidationError('User не существует!')

        try:
            confirmation_code = ConfirmationCode.objects.get(user=user)
        except ConfirmationCode.DoesNotExist:
            raise ValidationError('Код подтверждения не найден!')

        if confirmation_code.code != code:
            raise ValidationError('Неверный код подтверждения!')
        

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["email"] = user.email
        token["birthdate"] = user.birthdate.isoformat() if user.birthdate else None
        return token
    

class OauthCodeSerializer(serializers.Serializer):
    code = serializers.CharField()