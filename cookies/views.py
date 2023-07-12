from django.middleware.csrf import get_token

from rest_framework.views import APIView
from rest_framework.response import Response


class MyView(APIView):
    def post(self, request):
        return Response({"message": "Successful POST request!"})


class GetCSRFToken(APIView):
    def get(self, request):
        token = get_token(request)
        print(token)
        return Response({"token": token})
