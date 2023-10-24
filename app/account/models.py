from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    email = models.EmailField(unique=True)
    last_login = models.DateTimeField(null=True)
    last_request = models.DateTimeField(null=True)
    username = models.CharField(
        max_length=90,
        unique=False,
        default=email
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
