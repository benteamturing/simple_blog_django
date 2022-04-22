from django.contrib.auth import get_user_model

from rest_framework import serializers

from profiles.models import Profile


class UserSignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = (
            'username',
            'email',
            'password',
        )


class SignupSerializer(serializers.ModelSerializer):
    """
    회원가입에 필요한 User 필드와 Profile 필드를 한번에 serialize 한다.
    (nested 형태)
    """
    user = UserSignupSerializer(required=True)
    image = serializers.ImageField(
        max_length=None
    )

    class Meta:
        model = Profile
        field = ('user', 'nickname', 'desc', 'image')

    def create(self, validated_data):

        user_data = validated_data.pop('user')

        try:
            user_instance = get_user_model().objects.create(**user_data)
        except TypeError:
            raise TypeError

        validated_data['user'] = f'{user_instance.id}'

        profile_instance = Profile.objects.create(**validated_data)

        return profile_instance


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = (
            'id',
            'email',
            'date_joined',
        )
