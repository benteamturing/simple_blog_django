from django.db import models
from django.contrib.auth import get_user_model
from django_extensions.db.models import TimeStampedModel


class Profile(TimeStampedModel):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, related_name='profile')
    nickname = models.CharField(
        max_length=30,
        unique=True,
    )
    # TODO: URLField 이지만 확장자가 이미지가 아닌 경우 처리 로직
    image = models.URLField()
    desc = models.CharField(
        verbose_name='description',
        max_length=150,
        blank=True,
    )