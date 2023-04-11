from django.contrib.auth import logout
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from rest_framework import status
from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     ListAPIView, RetrieveAPIView,
                                     UpdateAPIView)
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import User
from users.serializers import UserSerializer
from auth.utils import account_activation_token


class UserListAPI(ListAPIView):
    """
        User list endpoint
        Role: Is admin user
    """
    permission_classes = [IsAdminUser]
    queryset = User.objects.all()
    serializer_class = UserSerializer
    

class UserAPI(RetrieveAPIView):
    """
        Retrieve a user endpoint
        Role: Is Authenticated
    """
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'uuid'
    

class UserCreateAPI(CreateAPIView):
    """
        User registration endpoint
    """
    permission_classes = [AllowAny]
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            new_user = serializer.save()
            
            current_site = get_current_site(request)
            mail_subject = "Activate your Fujyn account"
            message = render_to_string("activation_email.html", {
                'user': new_user,
                'domain': current_site.domain,
                'uid': new_user.uuid,
                'token': account_activation_token.make_token(new_user),
            })
            to_email = new_user.email
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()
    
            return Response(status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class ProfileAPI(APIView):
    """
        Account activation Endpoint
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request, format=None):
        user = request.user
        context={
            "uuid": user.uuid if user.uuid else None,
            "firstname": user.first_name if user.first_name else None,
            "lastname":user.last_name if user.last_name else None,
            "email":user.email,
            "username":user.username,
            "address":user.address if user.address else None,
            "city":user.city if user.city else None,
            "postal_code":user.postal_code if user.postal_code else None,
            "postal_code":user.date_joined if user.date_joined else None,
        }
    
        return Response(status=status.HTTP_200_OK, data=context)

    
class ActiveAccountAPI(APIView):
    """
        Account activation Endpoint
    """
    
    permission_classes = [AllowAny]
    
    def get(self, request, uidb64, token, format=None):
        user = User.objects.get(uuid=uidb64)
        if user and account_activation_token.check_token(user, token):
            user.is_active = True
            user.email_veridfied = True
            user.save()
            return Response(status=status.HTTP_202_ACCEPTED)
        

class ForgotPasswordAPI(APIView):
    """
        Forgot password endpoint
        Role: Allow Any
    """    
    permission_classes= [AllowAny]
    
    def post(self, request, format=None):
        user = User.objects.get(email=request.data['email'])
        current_site = get_current_site(request)
        mail_subject = "Reset your account password"
        message = render_to_string("password_reset_email.html", {
            'user': user,
            'domain': current_site.domain,
            'uid': user.uuid,
            'token': account_activation_token.make_token(user),
        })
        to_email = user.email
        email = EmailMessage(
            mail_subject, message, to=[to_email]
        )
        email.send()
        return Response({'status' : 'Success', 'message': 'We have sent you an email with the link to reset your password'},status=status.HTTP_200_OK)


class ResetPasswordAPI(APIView):
    """
        Reset Password API
        Role: Allow Any
    """
    permission_classes = [AllowAny]
    
    def post(self, request, uidb64, token, format=None):
        user = User.objects.get(uuid=uidb64)
        if not user.check_password(request.data['password1']) and request.data['password1'] == request.data['password2'] and account_activation_token.check_token(user, token):
            user.set_password(request.data['password1'])
            user.save()
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_403_FORBIDDEN)


class BlacklistAPI(APIView):
    """
        Blacklist user tokens
        Role: Allow Any
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request, format=None):
        refresh_token = request.data["refresh_token"]
        token = RefreshToken(refresh_token)
        token.blacklist()
        logout(request)
        return Response(status=status.HTTP_200_OK)


class UserUpdateAPI(UpdateAPIView):
    """
        Update user endpoint
        Role: Is Authenticated
    """
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'uuid'


class UserDeleteAPI(DestroyAPIView):
    """
        Delete user endpoint
        Role: Is Admin user
    """
    permission_classes = [IsAdminUser]
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'uuid'