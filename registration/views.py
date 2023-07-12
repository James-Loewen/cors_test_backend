from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import AnonymousUser, User

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import UserSerializer


class GetUser(APIView):
    def get(self, request):
        user = request.user
        if user.is_authenticated:
            serializer = UserSerializer(user)
            return Response(serializer.data)
        else:
            return Response(
                {"user": "anonymous"},
                status=status.HTTP_401_UNAUTHORIZED,
            )


class MyLoginView(APIView):
    def post(self, request):
        username = request.data.get("username", None)
        password = request.data.get("password", None)

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            serializer = UserSerializer(user)
            return Response(serializer.data)

        return Response(
            {"message": "Invalid credentials"},
            status=status.HTTP_401_UNAUTHORIZED,
        )


class MyLogoutView(APIView):
    def post(self, request):
        if type(request.user) is not AnonymousUser:
            logout(request)
            return Response({"message": "Successfully logged out!"})

        return Response(
            {"message": "A user was not logged in."},
            status=status.HTTP_400_BAD_REQUEST,
        )


class RegisterUser(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            login(request, user)

            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED,
            )

        else:
            return Response(
                {"message": "missing or invalid input"},
                status=status.HTTP_400_BAD_REQUEST,
            )
