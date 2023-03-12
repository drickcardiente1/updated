from django.utils import timezone
from django.utils.text import gettext_lazy as _
from drfaddons.utils import JsonResponse
from rest_framework import status, permissions
from rest_framework.exceptions import APIException
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework_simplejwt.settings import api_settings
from api.models import AuthTransaction
from api.models import User
from api.utils import validate_otp, generate_otp, login_user, send_otp, get_client_ip
from api.variables import *
from .serializers import *
from django.contrib.auth import login, logout
from rest_framework_simplejwt.tokens import AccessToken
import datetime
from rest_framework.renderers import JSONRenderer
# login
class LoginView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = CustomTokenObtainPairSerializer
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.user
        token = serializer.validated_data.get("access") 
        refresh_token = serializer.validated_data.get("refresh")
        AuthTransaction(created_by=user,token=str(token),refresh_token=str(refresh_token),ip_address=get_client_ip(self.request),session=user.get_session_auth_hash(),expires_at=timezone.now() + api_settings.ACCESS_TOKEN_LIFETIME,).save()
        resp = {"refresh_token": str(refresh_token),"token": str(token),"session": user.get_session_auth_hash(),}
        return Response(resp, status=status.HTTP_200_OK,)



# otp send request register
class OTPView(APIView):

    # renderer_classes = (JSONRenderer,)
    permission_classes = (AllowAny,)
    serializer_class = OTPSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        prop = EMAIL
        email = serializer.validated_data.get("email")
        otp_obj = generate_otp(prop, email)
        sentotp = send_otp(email, otp_obj, email)
        if sentotp["success"]:
            otp_obj.porpose = SIGNUP
            otp_obj.send_counter += 1
            otp_obj.save()
            return Response(sentotp, status=status.HTTP_201_CREATED)
        else:
             raise APIException(
                detail=_("A Server Error occurred: " + sentotp["message"])
            )

# register
class RegisterView(CreateAPIView):
    """
    Register View
    Register a new user to the system.
    The data required are username, email, otp, name, password and mobile (optional).
    """
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer
    def perform_create(self, serializer):
        otp = serializer.initial_data['otp']
        email = serializer.initial_data['email']
        validate_otp(email, otp)
        check_validation(value=email)
        data = {
            "username": serializer.validated_data["username"],
            "first_name": serializer.validated_data["first_name"],
            "last_name": serializer.validated_data["last_name"],
            "email": serializer.validated_data["email"],
            "password": serializer.validated_data["password"],
            "receive_notif": serializer.validated_data["receive_notif"],
        }
        return User.objects.create_user(**data)

# otp send request forgot password
class OTPViewForgotPassword(APIView):
    permission_classes = (AllowAny,)
    serializer_class = OTPSerializerForgotPassword

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        prop = EMAIL
        email = serializer.validated_data.get("email")
        otp_obj = generate_otp(prop, email)
        sentotp = send_otp(email, otp_obj, email)
        if sentotp["success"]:
            otp_obj.porpose = RESET
            otp_obj.send_counter += 1
            otp_obj.save()
            return Response(sentotp, status=status.HTTP_201_CREATED)
        else:
            raise APIException(
                detail=_("A Server Error occurred: " + sentotp["message"])
            )

# password reset
class PasswordResetView(APIView):
    """This API can be used to reset a user's password.

    Usage: First send an otp to the user by making an
    API call to `api/user/otp/` with `is_login` parameter value false.
    """

    serializer_class = PasswordResetSerializer
    permission_classes = (AllowAny,)
    def post(self, request, *args, **kwargs):
        """Overrides post method to validate OTP and reset password"""
        serializer = PasswordResetSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = User.objects.get(email=serializer.validated_data["email"])
        if validate_otp(serializer.validated_data["email"], serializer.validated_data["otp"]):
            # OTP Validated, Change Password
            user.set_password(serializer.validated_data["password"])
            user.save()
            return JsonResponse(
                content="Password Updated Successfully.",
                status=status.HTTP_202_ACCEPTED,
            )
            
            
class Profile(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        serializer = showProfileSerializer(request.user)
        return Response(serializer.data)

        
    
    



