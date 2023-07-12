from django.middleware.csrf import get_token

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class MyView(APIView):
    def post(self, request):
        return Response({"message": "Successful POST request!"})


class GetUser(APIView):
    def get(self, request):
        user = request.user
        if user.is_authenticated:
            return Response(
                {
                    "firstName": user.first_name,
                    "lastName": user.last_name,
                    "username": user.username,
                }
            )
        else:
            return Response(
                {"user": "anonymous"},
                status=status.HTTP_401_UNAUTHORIZED,
            )


class GetCSRFToken(APIView):
    def get(self, request):
        token = get_token(request)
        print(token)
        return Response({"token": token})
