from django.contrib.auth.models import AbstractUser
from django.db import models

NULLABLE = {'blank': True,
            'null': True}


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='почта')

    phone = models.CharField(max_length=35, verbose_name='телефон', **NULLABLE)
    country = models.CharField(max_length=35, verbose_name='страна', **NULLABLE)

    verification_key = models.IntegerField(verbose_name='ключ', **NULLABLE)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"{self.email}"

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'
