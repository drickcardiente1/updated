from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import Group
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils.text import gettext_lazy as _
from .managers import UserManager
from .variables import *
from django.core.validators import RegexValidator
import os, random
from datetime import datetime
from django.utils.html import format_html


class Role(Group):
    class Meta:
        proxy = True
        verbose_name = _("Role")
        verbose_name_plural = _("Roles")

def image_path(instance, filename):
    basefilename, file_extension = os.path.splitext(filename)
    char = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890'
    randstr = ''.join(random.choice(char) for x in range(10))
    _now = datetime.now()
    return 'profile_pic/{year}-{month}-{imageid}-{basename}-{randomstring}{ext}'.format(imageid = instance, basename = basefilename, randomstring = randstr, ext = file_extension, year = _now.strftime('%y'),month = _now.strftime('%m'), day = _now.strftime('%d'))


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField( verbose_name=_("Unique UserName"), max_length=254, unique=True )
    email = models.EmailField(verbose_name=_("Email Address"), unique=True)
    mobile = models.CharField( verbose_name=_("Mobile Number"), max_length=150, unique=True, null=True, blank=True, )
    first_name = models.CharField(verbose_name=_("First Name"),validators=[RegexValidator(regex=(r'^[A-Za-z]+$'),message='Username should be Contained Alphabitical',code='invalid_first_name'),], max_length=54, blank=False)
    last_name = models.CharField(verbose_name=_("Last Name"),validators=[RegexValidator(regex=(r'^[a-z A-Z]*$'),message='Username should be Contained Alphabitical',code='invalid_last_name'),], max_length=54, blank=False)
    type = models.CharField( verbose_name=_("Type (Admin/Renter)"), default=RENTER, max_length=3, choices=ACCOUNT_TYPE, )
    
    profile_image = models.ImageField(verbose_name=_("Profile Photo"), upload_to=image_path, default='profile_pic/default/default.avif', null=False, blank=True )
    address = models.CharField(verbose_name=_("Address"), max_length=50, null=True, blank=True, )
    city = models.CharField(verbose_name=_("City"), max_length=60, null=True, blank=True, )
    country = models.CharField(verbose_name=_("Country"), max_length=50, null=True, blank=True, )
    zipcode = models.CharField(verbose_name=_("Zip code"), max_length=5, null=True, blank=True, )
    About_Me = models.TextField(verbose_name=_("About Me"), max_length=700, null=True, blank=True, )

    date_joined = models.DateTimeField(verbose_name=_("Date Joined"), auto_now_add=True)
    update_date = models.DateTimeField(verbose_name=_("Date Modified"), auto_now=True)
    receive_notif = models.BooleanField(verbose_name=_("Notify me"),default=True)
    is_active = models.BooleanField(verbose_name=_("Activated"), default=False)
    is_staff = models.BooleanField(verbose_name=_("Staff Status"), default=False)
    is_admin = models.BooleanField(verbose_name=_("Admin"),default=False)
    is_client = models.BooleanField(verbose_name=_("Renter"),default=False)
    groups = models.ManyToManyField( Role, verbose_name=_("Roles"), blank=True, help_text=_("The roles this user belongs to. A user will get all permissions ""granted to each of their roles."), related_name="user_set", related_query_name="user", )
    objects = UserManager()
    USERNAME_FIELD = "username"
    
    REQUIRED_FIELDS = ["first_name", "last_name", "email"]
    class Meta:
        verbose_name = _("Accounts")
        verbose_name_plural = _("Accounts")
    # def image_tag(self):
    #     return format_html('<img src = "/media/profile_pic/{}" width="50" height="50" />'.format(self.profile_image))
    def get_first_name(self) -> str:
        return str(self.first_name)
    def __str__(self):
        return str(self.first_name) + " | " + str(self.username)
    def has_perm(self , perm, obj = None):
        return self.is_admin
    def has_module_perms(self , app_label):
        return True
    def save(self , *args , **kwargs):
        if self.type == ADMIN :
            self.is_active = True
            self.is_client = False
            self.is_admin = True
            self.is_staff = True
            self.is_superuser = True
        else:
            self.is_client = True
            self.is_admin = False
            self.is_staff = False
            self.is_superuser = False
        return super().save(*args , **kwargs)
    

class AuthTransaction(models.Model):
    ip_address = models.GenericIPAddressField(blank=False, null=False)
    token = models.TextField(verbose_name=_("JWT Access Token"))
    session = models.TextField(verbose_name=_("Session Passed"))
    refresh_token = models.TextField( blank=True, verbose_name=_("JWT Refresh Token"), )
    expires_at = models.DateTimeField( blank=True, null=True, verbose_name=_("Expires At") )
    create_date = models.DateTimeField( verbose_name=_("Create Date/Time"), auto_now_add=True )
    update_date = models.DateTimeField( verbose_name=_("Date/Time Modified"), auto_now=True )
    created_by = models.ForeignKey(to=User, on_delete=models.PROTECT, related_name='AuthTransaction')
    def __str__(self):
        return str(self.created_by.first_name) + " | " + str(self.created_by.username)
    class Meta:
        verbose_name = _("Authentication Transaction")
        verbose_name_plural = _("Authentication Transactions")
        
class OTPValidation(models.Model):
    otp = models.CharField(verbose_name=_("OTP Code"), max_length=10)
    destination = models.CharField( verbose_name=_("Destination Address (Mobile/EMail)"), max_length=254, unique=True, )
    porpose = models.CharField( verbose_name=_("Porpose (Signup/Reset)"), default=SIGNUP, max_length=3, choices=PORPOSE_CHOICES, )
    create_date = models.DateTimeField(verbose_name=_("Create Date"), auto_now_add=True)
    update_date = models.DateTimeField(verbose_name=_("Date Modified"), auto_now=True)
    is_validated = models.BooleanField(verbose_name=_("Is Validated"), default=False)
    validate_attempt = models.IntegerField( verbose_name=_("Attempted Validation"), default=3 )
    prop = models.CharField( verbose_name=_("Destination Property"), default=EMAIL, max_length=3, choices=DESTINATION_CHOICES, )
    send_counter = models.IntegerField(verbose_name=_("OTP Sent Counter"), default=0)
    sms_id = models.CharField( verbose_name=_("SMS ID"), max_length=254, null=True, blank=True )
    reactive_at = models.DateTimeField(verbose_name=_("ReActivate Sending OTP"))
    def __str__(self):
        return self.destination
    class Meta:
        verbose_name = _("OTP Validation")
        verbose_name_plural = _("OTP Validations")
