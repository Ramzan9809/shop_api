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
                is_active=False
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
            username=serializer.validated_data['username'],
            password=serializer.validated_data['password']
        )

        # step 2: Return Token (get or create)
        if user is not None:
            token_, _ = Token.objects.get_or_create(user=user)
            return Response(data={'key': token_.key})

        return Response(status=status.HTTP_401_UNAUTHORIZED)


class ConfirmUserAPIView(CreateAPIView):
    serializer_class = ConfirmationSerializer
    def post(self, request):
        serializer = ConfirmationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user_id = serializer.validated_data['user_id']

        with transaction.atomic():
            user = CustomUser.objects.get(id=user_id)
            user.is_active = True
            user.save()
