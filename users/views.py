from django.contrib.auth import authenticate
from .serializers import RegisterValidateSerializer, AuthValidateSerializer, ConfirmationSerializer
from .models import CustomUser 
from rest_framework.generics import CreateAPIView
from django.db import transaction
from rest_framework.response import Response
from rest_framework import status
import random
import string
from rest_framework.authtoken.models import Token
from .models import UserConfirmationCode as ConfirmationCode
from rest_framework_simplejwt.views import TokenObtainPairView
from users.serializers import CustomTokenObtainPairSerializer


class RegistrationAPIView(CreateAPIView):
    serializer_class = RegisterValidateSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        password = serializer.validated_data['password']

        # Use transaction to ensure data consistency
        with transaction.atomic():
            user = CustomUser.objects.create_user(
                email=email,
                password=password,
                phone_number=serializer.validated_data['phone_number'],
                birthdate=serializer.validated_data['birthdate'],
                is_active=True
            )

            # Create a random 6-digit code
            code = ''.join(random.choices(string.digits, k=6))

            confirmation_code = ConfirmationCode.objects.create(  # noqa: F841
                user=user,
                code=code
            )

        return Response(
            status=status.HTTP_201_CREATED,
            data={
                'user_id': user.id,
                'confirmation_code': code
            }
        )


class AuthorizationAPIView(CreateAPIView):
    serializer_class = AuthValidateSerializer
    def post(self, request):
        serializer = AuthValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # step 1: Authentication
        user = authenticate(
            email=serializer.validated_data['email'],
            password=serializer.validated_data['password']
        )

        # step 2: Return Token (get or create)
        if user is not None:
            token_, _ = Token.objects.get_or_create(user=user)
            return Response(data={'key': token_.key})

        return Response(status=status.HTTP_401_UNAUTHORIZED)


class ConfirmUserAPIView(CreateAPIView):
    serializer_class = ConfirmationSerializer
    def get_token(cls, user):
        token = super().get_token(user)
        token["email"] = user.email
        token["birthdate"] = str(user.birthdate) if user.birthdate else None
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        data['email'] = self.user.email
        data['birthdate'] = str(self.user.birthdate) if self.user.birthdate else None
        return data


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer