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

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

