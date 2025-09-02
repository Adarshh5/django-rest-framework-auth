from django.shortcuts import render

# Create your views here.
# users/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings
from django.urls import reverse
from account.models import User
from .serializers import RegisterSerializer, LoginSerializer
from .utils.email import send_activation_email

from .serializers import PasswordResetRequestSerializer, PasswordResetConfirmSerializer, UserSerializer
from .utils.email import send_reset_password_email
from rest_framework.permissions import IsAuthenticated
import datetime
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from django.core.cache import cache





class RegisterAPIView(APIView):
    permission_classes = []  # anyone can register

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            activation_link = reverse("users:activate", kwargs={"uidb64": uidb64, "token": token})
            activation_url = f"{settings.SITE_DOMAIN}{activation_link}"

            send_activation_email(user.email, activation_url)

            return Response(
                {"detail": "Registration successful! Check your email to activate your account."},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ActivateAPIView(APIView):
    permission_classes = []  # allow anyone with link

    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return Response({"detail": "Invalid activation link."}, status=status.HTTP_400_BAD_REQUEST)

        if user.is_active:
            return Response({"detail": "This account is already active."}, status=status.HTTP_200_OK)

        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return Response({"detail": "Your account has been activated successfully!"}, status=status.HTTP_200_OK)

        return Response({"detail": "Activation link is invalid or expired."}, status=status.HTTP_400_BAD_REQUEST)




class LoginAPIView(APIView):
    permission_classes = []  # allow anyone

    def post(self, request):
        serializer = LoginSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            tokens_and_user = serializer.save()
            return Response(tokens_and_user, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





class PasswordResetRequestAPIView(APIView):
    permission_classes = []

    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data["email"]
            user = User.objects.get(email=email)

            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            reset_link = reverse("users:password_reset_confirm", kwargs={"uidb64": uidb64, "token": token})
            reset_url = f"{settings.SITE_DOMAIN}{reset_link}"

            send_reset_password_email(user.email, reset_url)
            return Response(
                {"detail": "We have sent you a password reset link. Please check your email."},
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetConfirmAPIView(APIView):
    permission_classes = []

    def post(self, request, uidb64, token):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save(uidb64, token)
                return Response({"detail": "Password has been reset successfully."}, status=status.HTTP_200_OK)
            except serializers.ValidationError as e:
                return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    




class MeAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
    







class LogoutAPIView(APIView):
    def post(self, request):
        refresh_token = request.data.get("refresh")
        access_token = request.data.get("access")

        if access_token:
            try:
                token = AccessToken(access_token)
                exp = token['exp']
                jti = token['jti']

                # Store in Redis until token expires
                ttl = exp - int(datetime.datetime.utcnow().timestamp())
                cache.set(f"blacklist_{jti}", "true", timeout=ttl)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        if refresh_token:
            try:
                RefreshToken(refresh_token).blacklist()
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"detail": "Successfully logged out."}, status=status.HTTP_200_OK)



