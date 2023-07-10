from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response


class MyView(APIView):
    def get(self, request):
        return Response({'message': 'Oh boy, a view!'})


class GetUser(APIView):
    def get(self, request):
        if request.user.is_authenticated:
            return Response({'current user:': request.user.username})
        else:
            return Response({'current user:': 'anonymous'})
