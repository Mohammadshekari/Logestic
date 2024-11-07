from rest_framework.response import Response
from rest_framework import generics, status, views, mixins
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework.serializers import Serializer
from .serializers import *
import jwt
from django.conf import settings
# from ...utils import Util
from django.contrib.sites.shortcuts import get_current_site
from rest_framework_simplejwt.tokens import RefreshToken
from django.urls import reverse
from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken

class RegisterApiView(generics.GenericAPIView):

    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            user = User.objects.get(email=serializer.validated_data['email'])
            token = RefreshToken.for_user(user).access_token
            current_site = get_current_site(request).domain
            relativeLink = reverse('accounts:email_verify')
            absurl = 'http://'+current_site+relativeLink+"?token="+str(token)
            # email_body = 'Hi '+user.email + \
            #     ' Use the link below to verify your email \n' + absurl
            # data = {'email_body': email_body, 'to_email': user.email,
            #         'email_subject': 'Verify your email'}
            #  Util.send_email(data)
            # data = {'email':user.email,"link":absurl,"site":current_site}
            # Util.send_templated_email('emails/verification_template.html',data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)


class VerifyEmailApiView(generics.GenericAPIView):
    serializer_class = EmailVerificationSerializer
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        if not user.is_verified:
            user.is_verified = True
            user.save()
        return Response({"detail":"user verified successfully"},status=status.HTTP_200_OK)


class ChangePasswordView(mixins.UpdateModelMixin, generics.GenericAPIView):
    """
    An endpoint for changing password.
    """
    serializer_class = ChangePasswordSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def put(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'details': 'Password updated successfully',
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class JWTObtainPairTokenApiView(generics.CreateAPIView):
    serializer_class = JWTObtainPairTokenSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        refresh = RefreshToken.for_user(user)
        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'user_id': user.pk,
            'email': user.email
        })


class ResendVerifyEmailApiView(generics.GenericAPIView):

    serializer_class = ResendVerifyTokenSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data["instance"]
            token = RefreshToken.for_user(user).access_token
            current_site = get_current_site(request).domain
            relativeLink = reverse('accounts:email_verify')
            absurl = 'http://'+current_site+relativeLink+"?token="+str(token)
            # email_body = 'Hi '+user.email + \
            #     ' Use the link below to verify your email \n' + absurl
            # data = {'email_body': email_body, 'to_email': user.email,
            #         'email_subject': 'Verify your email'}
            # data = {'email':user.email,"link":absurl,"site":current_site}
            #  Util.send_email(data)
            data = {'email':user.email,"link":absurl,"site":current_site}
            # Util.send_templated_email('emails/verification_template.html',data)
           
            return Response({"details":"verification mail has been sent"}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetRequestEmailApiView(generics.GenericAPIView):
    serializer_class = PasswordResetRequestEmailSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token = RefreshToken.for_user(user).access_token
        relativeLink = "/accounts/reset-password" #reverse('accounts:password-reset-confirm')
        current_site = get_current_site(
            request=request).domain
        absurl = 'http://'+current_site+relativeLink+"?token="+str(token)
        # email_body = 'Hi '+user.email + \
        #         'Use the link below to reset your password \n' + absurl
        # data = {'email_body': email_body, 'to_email': user.email,
        #             'email_subject': 'Verify your email'}

        # Util.send_email(data)
        data = {'email':user.email,"link":absurl,"site":current_site}
        # Util.send_templated_email('emails/reset_password_template.html',data)
        return Response({'success': 'We have sent you a link to reset your password'}, status=status.HTTP_200_OK)


class PasswordResetTokenValidateApiView(mixins.RetrieveModelMixin, generics.GenericAPIView):
    serializer_class = PasswordResetTokenVerificationSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response({"detail":"Token is valid"},status=status.HTTP_200_OK)


class PasswordResetSetNewApiView(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer

    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'detail': 'Password reset successfully'}, status=status.HTTP_200_OK)