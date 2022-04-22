from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from profiles.models import Profile


class ProfileSerializer(ModelSerializer):
    """
    Profile list 혹은 Profile detail에 표시될 정보를 직렬화한다.
    nickname, desc, img_src 등
    """

    # 이미지를 저장하고 있는 S3 저장소의 URL을 들고온다.
    img_src = serializers.ReadOnlyField(source='absolute_image_url')
    created = serializers.ReadOnlyField()

    class Meta:
        model = Profile
        fields = ('nickname', 'desc', 'img_src')

