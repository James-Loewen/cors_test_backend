from django.contrib.auth.models import User

from rest_framework.serializers import ModelSerializer


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "first_name", "last_name", "username", "password"]

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
