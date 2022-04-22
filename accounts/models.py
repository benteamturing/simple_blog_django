from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models


class CustomUserManager(UserManager):

    def get_query_set(self):
        return super(
            CustomUserManager,
            self
        ).get_query_set(
        ).filter(
            is_active=True
        )


class CustomUser(AbstractUser):
    """
    django 기본 인증 시스템을 이용하기 위한 User모델
    소셜로그인 구현을 위해, username이 아닌 email을 unique identifier로 설정
    username을 받지 않는 경우 django-admin page와 충돌이 일어나 받기는 받지만 쓰진 않음.
    active한 계정을 불러오기 위해서는 active_objects를 이용한다.
    user model을 부르기 위해서는 django.contrib.auth.get_user_model()을 이용해 호출한다.
    """
    # email을 unique identifier로 설정한다.
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    # email과 password로 계정을 생성한 후 username이 unique로 되어 있어서 생기는 오류를 방지한다.
    username = models.CharField(
        max_length=120,
        blank=True,
        unique=False
    )
    # 필요 없는 필드들
    first_name = None
    last_name = None

    active_objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

