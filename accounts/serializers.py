from django.contrib.auth import get_user_model

from rest_framework import serializers


class UserSignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = (
            'username',
            'email',
            'password',
        )


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = (
            'id',
            'email',
            'date_joined',
        )
