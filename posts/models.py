from django.db import models
from django_extensions.db.models import TimeStampedModel

from profiles.models import Profile


class ActivePostManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(profile__user__is_active=True)


class Post(TimeStampedModel):
    """
    created와 modified를 상속을 통해 받음
    게시판은 제목, 내용, 작성자로 구성된다.
    """
    title = models.CharField(
        max_length=40
    )
    content = models.TextField()
    profile = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name='post'
    )

    objects = models.Manager()
    active_objects = ActivePostManager()

    def __str__(self):
        return f'{self.title}'

    @property
    def summary(self):
        """
        summary of body contents
        """
        return self.get_summary()

    def get_summary(self):
        """
        get summary of body contents
        """
        return f'{self.content}'[:75]
