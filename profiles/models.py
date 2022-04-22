from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django_extensions.db.models import TimeStampedModel

from common import generate_random_filename


class CustomProfileManager(models.Manager):
    """
    연결된 user가 active인 profile들만 쿼리하는 매니저
    """
    def get_queryset(self):
        return super().get_queryset().filter(user__is_active=True)


class Profile(TimeStampedModel):
    """
    게시판 작성자의 프로필 정보를 표현하기 위한 모델
    :fields: nickname, desc, image
    :nickname: unique identifer, 유저의 닉네임
    :desc: 상태메시지/ 자기소개 (150자 제한)
    :image: 프로필 이미지
    :user: user와 1대1 관계
    :prefix: property, 이미지 파일 저장 디렉토리
    :absolute_image_url: property, 이미지 파일 절대 저장 경로
    Note: user가 inactive인 경우 profile도 검색 되지 않도록 해야함
    -> active_objects 모델 매니저 사용 권장
    """
    user = models.OneToOneField(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='profile'
    )
    nickname = models.CharField(
        max_length=30,
        unique=True
    )
    desc = models.CharField(
        max_length=150,
        null=True,
        verbose_name='description'
    )
    image = models.ImageField(
        upload_to=generate_random_filename,
        default='/default_profile_image.png'
    )

    objects = models.Manager()
    active_objects = CustomProfileManager()

    def __str__(self):
        return f'{self.nickname}'

    @property
    def prefix(self):
        """
        파일이 저장될 상대경로
        """
        return self.get_file_path_prefix()

    @property
    def absolute_image_url(self):
        """
        파일이 저장된 절대 경로
        """
        return self.get_absolute_image_url()

    def get_absolute_image_url(self):
        """
        파일이 저장된 절대 경로를 생성한다.
        """
        return f'{settings.MEDIA_URL}{self.image.url}'[1:]

    def get_file_path_prefix(self):
        """
        파일이 저장될 상대경로를 가져온다.
        """
        return f'profile_images/{self.nickname}'


