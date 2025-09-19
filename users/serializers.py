from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.exceptions import ValidationError
from .models import UserConfirmationCode


class AuthValidateSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class RegisterValidateSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate_username(self, username):
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        raise ValidationError('User already exists!')
    


class ConfirmCodeSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    code = serializers.CharField(max_length=6)

    def validate(self, attrs):
        user_id = attrs.get('user_id')
        code = attrs.get('code')

        try:
            confirmation = UserConfirmationCode.objects.get(user_id=user_id)
        except UserConfirmationCode.DoesNotExist:
            raise ValidationError('Confirmation code not found for this user.')

        if confirmation.code != code:
            raise ValidationError('Invalid confirmation code.')

        attrs['user'] = confirmation.user  # добавляем объект user для использования в view
        attrs['confirmation'] = confirmation  # добавляем объект confirmation
        return attrs