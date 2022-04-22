from django.contrib.auth import get_user_model

from rest_framework import serializers

from profiles.models import Profile


def get_user_id_or_raise_type_error(**user_data):
    try:
        user_instance = get_user_model().objects.create(**user_data)
        return user_instance.id
    except TypeError:
        raise TypeError


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
        # nested serializer에서 user serializer data를 뽑아낸다
        user_data = validated_data.pop('user')

        # user serializer data로 user instance 생성을 시도한다.
        user_id = get_user_id_or_raise_type_error(**user_data)

        # user id를 profile serializer data에 삽입한다.
        validated_data['user'] = f'{user_id}'

        # profile을 생성한다.
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
