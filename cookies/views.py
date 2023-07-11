from django.middleware.csrf import get_token

from rest_framework.views import APIView
from rest_framework.response import Response


class MyView(APIView):
    def get(self, request):
        return Response({'message': 'Oh boy, a view!'})


class GetUser(APIView):
    def get(self, request):
        if request.user.is_authenticated:
            return Response({'user': request.user.username})
        else:
            return Response({'user': 'anonymous'})


class GetCSRFToken(APIView):
    def get(self, request):
        token = get_token(request)
        print(token)
        return Response({'token': token})
