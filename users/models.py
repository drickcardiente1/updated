from django.db import models
from api.models import User
from .managers import *
from django.utils.text import gettext_lazy as _
from datetime import datetime
import os, random


def image_path(instance, filename):
    basefilename, file_extension = os.path.splitext(filename)
    char = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890'
    randstr = ''.join(random.choice(char) for x in range(10))
    _now = datetime.now()
    return 'profile_pic/{year}-{month}-{imageid}-{basename}-{randomstring}{ext}'.format(imageid = instance, basename = basefilename, randomstring = randstr, ext = file_extension, year = _now.strftime('%y'),month = _now.strftime('%m'), day = _now.strftime('%d'))

class client(User):
    class Meta :
        proxy = True
        verbose_name = _("Renters")
        verbose_name_plural = _("Renters")
    objects = ClientManager()
    def save(self , *args , **kwargs):
        self.is_client = True
        self.is_admin = False
        self.is_staff = False
        self.is_superuser = False
        return super().save(*args , **kwargs)

class User_profile(models.Model):
    created_by = models.ForeignKey(to=User, on_delete=models.PROTECT, related_name='profile_picture')
    profile_image = models.ImageField(verbose_name=_("Profile Photos"), upload_to=image_path, default='profile_pic/default/default.avif', null=False, blank=True )
    class Meta:
        verbose_name = _("User Profile Images")
        verbose_name_plural = _("User Profile Images")
    

    
