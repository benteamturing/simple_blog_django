from django.db import models
from django_extensions.db.models import TimeStampedModel


class Post(TimeStampedModel):
    title = models.CharField(max_length=100)
    content = models.TextField(max_length=2000)

    @property
    def summary(self):
        return self.get_summary()

    def get_summary(self):
        return f'{self.title}'


