from django.core.validators import (EmailValidator, MinLengthValidator)
from django.contrib.auth.models import AbstractUser 
from django.db import models
import uuid


class Usuario(AbstractUser):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length = 200, blank=False)
    last_name = models.CharField(max_length = 200, blank=False)
    email = models.CharField(max_length = 200, unique=True, blank=False, validators=[
        EmailValidator(message=None, code=None, whitelist=None)])
    username = models.CharField(max_length = 200, unique=False, default='')
    password = models.CharField(max_length = 200, blank=False, validators=[
        MinLengthValidator(limit_value=8, message=None)])
    is_active = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.first_name