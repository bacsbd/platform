from django.db import models
from django.contrib.auth.models import (
    AbstractUser
)
# Create your models here.


class User(AbstractUser):
    email = models.CharField(db_index=True, max_length=255, unique=True)
    first_name = models.CharField(max_length=31)
    last_name = models.CharField(max_length=31)
    address = models.CharField(max_length=255, default="")
    institution = models.CharField(max_length=255)
    role = models.CharField(max_length=15)
    tshirt_size = models.CharField(max_length=4, default="L")
    division = models.CharField(db_index=True, max_length=10)
    verified = models.BooleanField(default=True)
