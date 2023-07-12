from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import AnonymousUser, User

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


# Create your views here.
class MyLoginView(APIView):
    def post(self, request):
        username = request.data.get("username", None)
        password = request.data.get("password", None)

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return Response(
                {
                    "firstName": user.first_name,
                    "lastName": user.last_name,
                    "username": user.username,
                }
            )

        return Response(
            {"message": "Invalid credentials"}, status=status.HTTP_401_FORBIDDEN
        )


class MyLogoutView(APIView):
    def post(self, request):
        if type(request.user) is not AnonymousUser:
            logout(request)
            return Response({"message": "Successfully logged out!"})

        return Response(
            {"message": "A user was not logged in."}, status=status.HTTP_400_BAD_REQUEST
        )


class RegisterUser(APIView):
    def post(self, request):
        try:
            username = request.data["username"]
            password = request.data["password"]

            user = User.objects.create_user(username=username, password=password)
            user.save()

            login(request, user)
            return Response(
                {
                    "firstName": user.first_name,
                    "lastName": user.last_name,
                    "username": user.username,
                },
                status=status.HTTP_201_CREATED,
            )
        except KeyError:
            return Response(
                {"message": "missing or invalid input"},
                status=status.HTTP_400_BAD_REQUEST,
            )
