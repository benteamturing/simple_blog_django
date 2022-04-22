from django.db import models
from django_extensions.db.models import TimeStampedModel

from profiles.models import Profile


class Post(TimeStampedModel):
    title = models.CharField(
        max_length=40
    )
    content = models.TextField()
    profile = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name='post'
    )

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
