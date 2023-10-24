from django.contrib.auth import authenticate, login

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from validate_email_address import validate_email
from account.api.serializers import UserActivitySerializer


User = get_user_model()


class RegistrationView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            return Response(
                {'message': 'You must add email and password to your request.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not validate_email(email):
            return Response(
                {'message': 'Invalid email.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            validate_password(password)
        except ValidationError:
            return Response(
                {'message': 'Password is too easy.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if User.objects.filter(email=email).exists():
            return Response(
                {'message': 'This email is registered already.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = User(email=email)
        user.set_password(password)
        user.save()

        login(request, user)
        return Response(
            {'message': 'You have successfully been registered.'},
            status=status.HTTP_201_CREATED
        )


class LoginView(APIView):

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            return Response(
                {'message': 'You must add email and password to your request.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return Response(
                {'message': 'Complete!'},
                status=status.HTTP_200_OK
            )
        else:
            return Response({'message': 'Incorrect email or password.'}, status=status.HTTP_401_UNAUTHORIZED)


class UserActivityView(APIView):

    def get(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response(
                {"message": "There are no user with this ID."},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = UserActivitySerializer(user)
        return Response(serializer.data)
