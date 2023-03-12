from api.models import User
from api.variables import *
from django.db import models

# client Manager
class ClientManager(models.Manager):
    def create_user(self, username, email, password, **extra_fields):
        if not email or len(email) <= 0 :
            raise  ValueError("Email field is required !")
        if not password :
            raise ValueError("Password is must !")
        user = self._create_user(username, email, password, False, False, **extra_fields)
        self.is_client = True
        self.is_admin = False
        self.is_staff = False
        self.is_superuser = False
        user.set_password(password)
        user.save(using=self._db)
        return user
    def get_queryset(self , *args,  **kwargs):
        queryset = super().get_queryset(*args , **kwargs)
        queryset = queryset.filter(type = RENTER)
        return queryset
    