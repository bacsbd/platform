import uuid

from django.db import models
from django.contrib.auth.models import (
    AbstractUser
)

from theplatform.models import BaseModel

class User(AbstractUser):
    email = models.CharField(db_index=True, max_length=255, unique=True)
    first_name = models.CharField(max_length=31)
    last_name = models.CharField(max_length=31)
    address = models.CharField(max_length=255, default="")
    institution = models.CharField(max_length=255)
    role = models.CharField(max_length=15)
    tshirt_size = models.CharField(max_length=4, default="L")
    division = models.CharField(db_index=True, max_length=10)
    verified = models.BooleanField(default=False)



class APIAuth(BaseModel):
    secret = models.CharField(db_index=True, max_length=255, unique=True, default= str(uuid.uuid4().hex))
    valid = models.BooleanField(default=True)
    description = models.CharField(db_index=True, max_length=255, default="")
