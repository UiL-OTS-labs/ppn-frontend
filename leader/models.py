from django.db import models

from api.auth.models import RemoteApiUser


class LeaderPhoto(models.Model):

    leader = models.ForeignKey(
        RemoteApiUser,
        on_delete=models.CASCADE
    )

    photo = models.ImageField(
        blank=True
    )
