from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
import random
from .serializers import RegisterValidateSerializer, AuthValidateSerializer, ConfirmCodeSerializer
from .models import UserConfirmationCode


class RegistrationAPIView(APIView):
    def post(self, request):
        # step 0: Validation
        serializer = RegisterValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={'errors': serializer.errors}
            )

        # step 1: Create user
        user = User.objects.create_user(
            username=serializer.validated_data['username'],
            password=serializer.validated_data['password'],
            is_active=False
        )

        # step 1a: Generate 6-digit confirmation code and save
        code = str(random.randint(100000, 999999))
        UserConfirmationCode.objects.create(user=user, code=code)

        # step 2: Return response
        return Response(
            status=status.HTTP_201_CREATED,
            data={'user_id': user.id, 'confirmation_code': code}
        )


class AuthorizationAPIView(APIView):
    def post(self, request):
        # step 0: Validation
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


class ConfirmRegistrationAPIView(APIView):
    def post(self, request):
        serializer = ConfirmCodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']
        confirmation = serializer.validated_data['confirmation']

        # Активируем пользователя
        user.is_active = True
        user.save()

        # Удаляем код
        confirmation.delete()

        return Response(
            status=status.HTTP_200_OK,
            data={'message': 'User successfully activated'}
        )
