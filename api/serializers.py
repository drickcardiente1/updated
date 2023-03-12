from django.contrib.auth.password_validation import validate_password, password_changed
from django.core.validators import EmailValidator
from django.core.validators import ValidationError
from django.utils.text import gettext_lazy as _
from rest_framework import serializers
from rest_framework.exceptions import NotFound
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.serializers import (ModelSerializer,)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
)

from api import user_settings
from api.models import User, OTPValidation
from api.utils import *
from api.variables import *
from rest_framework.exceptions import APIException


# login
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Custom Token Obtain Pair Serializer
    Custom serializer subclassing TokenObtainPairSerializer to add
    certain extra data in payload such as: email, mobile, name
    """
    default_error_messages = {
        "no_active_account": _("username or password is invalid.")
    }
    @classmethod
    def get_token(cls, user):
        """Generate token, then add extra data to the token."""
        token = super().get_token(user)
        # Add custom claims
        if hasattr(user, "email"):
            token["email"] = user.email
        if hasattr(user, "mobile"):
            token["mobile"] = user.mobile
        if hasattr(user, "name"):
            token["name"] = user.name
        return token

# otp send request register
class OTPSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    def validate_email(self, email: str) -> str:
        is_already_exists = User.objects.filter(email=email).exists()
        if is_already_exists:
            raise serializers.ValidationError('This email is already registered')
        return email
    def get_user(self, email: str) -> User:
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            user = None
        return user

# sign up
class UserSerializer(serializers.ModelSerializer):
    otp = serializers.CharField(required=True)
    receive_notifications = serializers.BooleanField(source='receive_notif')
    def validate(self, data):
        errors = {}
        email = data["email"]
        if check_email(value = email, porpose = SIGNUP) is False:
            errors["email"] = [_("No pending OTP validation request found for provided ""Email. Kindly send an OTP first")]
        if not validate_password(data["password"]) is None:
            errors["password"] = [_("This field must match")]
        if errors:
            raise serializers.ValidationError(errors)
        return data

    def validate_otp(self, value: str) -> str:
        email = self.initial_data['email']
        if check_otp(email, value) is "3":
            otp_object: OTPValidation = OTPValidation.objects.get(destination=email, is_validated=False)
            raise serializers.ValidationError(
                f"OTP Validation failed! {otp_object.validate_attempt} attempts left!"
            )
        if check_otp(email, value) is "2":
            otp_object: OTPValidation = OTPValidation.objects.get(destination=email, is_validated=False)
            validate_otp(email, value)
            raise AuthenticationFailed(
                    detail=_("Incorrect OTP. Attempt exceeded! OTP has been reset.")
                )
        return value

    def validate_email(self, value: str) -> str:
        if not user_settings["EMAIL_VALIDATION"]:
            return value
        if check_email(value = value,  porpose = SIGNUP):
            return value
        else:
            raise serializers.ValidationError(
                "No pending OTP validation request found for provided ""Email. Kindly send an OTP first"
            )

    def validate_password(self, value: str) -> str:
        validate_password(value)
        return value

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "otp",
            "username",
            "first_name",
            "last_name",
            "mobile",
            "password",
            "receive_notifications",
            "is_superuser",
            "is_staff",
        )
        read_only_fields = ("is_superuser", "is_staff")
        extra_kwargs = {"password": {"write_only": True}}


# otp send request forgot password
class OTPSerializerForgotPassword(serializers.Serializer):
    email = serializers.EmailField(required=True)
    def validate_email(self, email: str) -> str:
        is_already_exists = User.objects.filter(email=email).exists()
        if not is_already_exists:
            raise serializers.ValidationError('This email is not registered')
        return email



# password reset
class PasswordResetSerializer(serializers.ModelSerializer):

    otp = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)

    def validate_email(self, value: str) -> str:
        if not user_settings["EMAIL_VALIDATION"]:
            return value
        if check_email(value = value,  porpose = RESET):
            return value
        else:
            raise serializers.ValidationError(
                "No pending OTP validation request found for provided ""Email. Kindly send an OTP first"
            )

    def validate_password(self, value: str) -> str:
        validate_password(value)
        return value

    def validate(self, data):
        errors = {}
        email = data["email"]
        otp = data["otp"]
        validator = EmailValidator()
        validator(email)
        user = self.get_user(email)
        if not user:
            errors["email"] = [_("No pending OTP validation request found for provided ""Email. Kindly send an OTP first")]
        email = self.initial_data['email']
        if check_otp(email, otp) is "3":
            otp_object: OTPValidation = OTPValidation.objects.get(destination=email, is_validated=False)
            raise serializers.ValidationError(
                f"OTP Validation failed! {otp_object.validate_attempt} attempts left!"
            )
        if check_otp(email, otp) is "2":
            otp_object: OTPValidation = OTPValidation.objects.get(destination=email, is_validated=False)
            otp_obj = generate_otp(otp_object.prop, email)
            send_otp(email, otp_obj, email)
            raise AuthenticationFailed(
                    detail=_("Incorrect OTP. Attempt exceeded! OTP has been reset.")
                )
        if errors:
            raise serializers.ValidationError(errors)
        return data

    def get_user(self, destination: str) -> User:
        try:
            user = User.objects.get(email=destination)
        except User.DoesNotExist:
            user = None
        return user

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "otp",
            "password",
        )
        read_only_fields = ("is_superuser", "is_staff")
        extra_kwargs = {"password": {"write_only": True}}

class showProfileSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "password",
            "address",
            "city",
            "country",
            "zipcode",
            "About_Me",
            "profile_image",
            "type",
        )




    

