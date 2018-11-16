import hashlib

from django.utils import timezone
import random
from _sha256 import sha256
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from django.core.mail import EmailMultiAlternatives
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from accounts import models
from django.core.exceptions import ObjectDoesNotExist
from .serializers import UserCreateSerializer, UserSerializer, ForgotPasswordResetSerializer,\
    ResetForgotPasswordSerializer, UserUpdateSerializer, PasswordResetSerializer
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics


class UserCreateView(generics.CreateAPIView):
    serializer_class = UserCreateSerializer
    queryset = User.objects.all()
    permission_classes = []
    authentication_classes = []

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            hash_code = sha256((str(random.getrandbits(256)) + serializer.validated_data.get('email')).encode('utf-8')).hexdigest()
            user = User.objects.get(email=serializer.validated_data.get('email'))
            models.MailVerification(user=user, link=hash_code, request_type=0).save()
            subject, from_mail, to = 'Verification mail at IoT', 'rammanojpotla1608@gmail.com', \
                                     serializer.validated_data.get('email', None)
            message= 'We received a request to the registration from this account, ' \
                     'please <a href="http://127.0.0.1:8000/accounts/mailverify/' + hash_code + '/">' \
                     'click here</a> to confirm it.'
            mail = EmailMultiAlternatives(
                subject,
                'Click link to finish registration',
                from_mail,
                [to],
            )
            mail.attach_alternative(message, 'text/html')
            mail.send()
            return Response({'message': 'Confirm the verification mail, will be sent to your mail in few minutes',
                             'success': 1}, status=status.HTTP_200_OK)
        else:
            return Response({'errors': serializer.errors, 'success': 0}, status=status.HTTP_400_BAD_REQUEST)


class UserUpdateView(generics.UpdateAPIView):
    serializer_class = UserUpdateSerializer

    def get_queryset(self):
        print(self.kwargs['pk'])
        return User.objects.filter(pk=self.kwargs['pk'])

    def partial_update(self, request, *args, **kwargs):
        if self.get_object() != request.user:
            return Response({'error': 'permission denied'}, status=status.HTTP_400_BAD_REQUEST)

        instance = super(UserUpdateView, self).partial_update(request, *args, **kwargs)
        instance.data['message'] = 'successfully updated profile!'
        return instance


class UserView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        if self.get_object() != request.user:
            return Response({'error': 'Permission denied'})
        else:
            return super(UserView, self).get(self, request, *args, **kwargs)

    def get_queryset(self):
        return User.objects.all()


@api_view(['POST'])
@csrf_exempt
@permission_classes((AllowAny,))
def password_reset(request):
    reset = ResetForgotPasswordSerializer(data=request.data)
    if reset.is_valid():
        email = reset.validated_data.get('email')
        try:
            user = User.objects.get(email=email)
        except ObjectDoesNotExist:
            return Response({'error': 'Please recheck your email'})
        try:
            verify = models.MailVerification.objects.get(user=user)
        except ObjectDoesNotExist:
            verify = models.MailVerification.objects.create(user=user)
        hash_code = sha256((str(random.getrandbits(256)) + email).encode('utf-8')).hexdigest()
        verify.link = hash_code
        verify.request_type = 2
        verify.save()
        subject, from_mail, to = 'Forgot password', 'rammanojpotla1608@gmail.com', email
        message = 'We received a request to the password forget from this account, ' \
                  'please <a href="http://localhost/templates/html/password_reset.html">' \
                  'click here</a> to reset it.'
        mail = EmailMultiAlternatives(
            subject,
            'Click link to reset password',
            from_mail,
            [to],
        )
        mail.attach_alternative(message, 'text/html')
        mail.send()

        return Response({'message': 'A verification mail has been sent to your mail account, please confirm it',
                         'token': hash_code})


@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def login(request):
    username = request.data.get('username', None)
    password = request.data.get('password', None)
    print(timezone.now() + timezone.timedelta(days=1))
    if (username is None or username == "") or (password is None or password == ""):
        return Response({'error': 'Enter valid credentails'})

    user = authenticate(username=username, password=password)
    if not user:
        return Response({'error': 'No user found as per given requirements'})

    if Token.objects.filter(user=user).exists():
        return Response({'error': 'You are already logged-in'}, status=status.HTTP_400_BAD_REQUEST)

    token, tk = Token.objects.get_or_create(user=user) # if token found, use it else create new token to the user
    # tk is True on creating a new tuple,
    return Response({
        'token': token.key,
        'user': user.pk
    }, status=status.HTTP_200_OK)


class Logout(generics.DestroyAPIView):

    def get_queryset(self):
        if self.request.user is not None:
            return User.objects.all()
        else:
            return User.objects.none()

    def post(self, request):
        if request.user is not None:
            request.user.auth_token.delete()
            return Response({'message': 'Successfully logout.'})
        else:
            return Response({'message': 'Already logged out'})


@api_view(['GET'])
@csrf_exempt
@permission_classes((AllowAny,))
def mail_verify(self, verify_id):
    try:
        user_mail = models.MailVerification.objects.get(link=verify_id)
    except ObjectDoesNotExist:
        return Response({'error': 'Your mail already verified, please login to continue'})

    if user_mail.user.is_active is True:
        return Response({'error': 'Your mail already verified, please login to continue'},
                        status=status.HTTP_400_BAD_REQUEST)
    else:
        user_mail.user.is_active = True
        user_mail.user.save()
        return Response({'message': 'Your mail successfully verified.'}, status=status.HTTP_200_OK)


class ForgotPasswordResetView(generics.UpdateAPIView):
    lookup_field = 'link'
    serializer_class = ForgotPasswordResetSerializer
    permission_classes = []
    authentication_classes = []

    def get_queryset(self):
        try:
            queryset = models.MailVerification.objects.filter(link=self.kwargs.get('link', None))
            print(queryset)
        except ObjectDoesNotExist:
            queryset = models.MailVerification.objects.none()

        return queryset

    def update(self, request, *args, **kwargs):
        return Response({'detial': 'Method PUT not allowed'})

    def partial_update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            if not self.get_queryset() or not (self.get_queryset()[0].request_type == 2):
                return Response({'error': 'perform a password change operaiton first.'})
            if (self.get_queryset()[0].link_expire + timezone.timedelta(days=1)) < timezone.now():
                self.get_queryset().delete()
                return Response({'error': 'The link has expired, please try again'})
            user = User.objects.get(pk=self.get_queryset()[0].user.pk)
            user.set_password(serializer.validated_data['password'])
            user.save()
            self.get_queryset().delete()
            return Response({'message': 'Password successfully updated'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetView(generics.UpdateAPIView):
    serializer_class = PasswordResetSerializer

    def get_queryset(self):
        return User.objects.filter(pk=self.kwargs['pk'])

    def partial_update(self, request, *args, **kwargs):

        if self.get_object() != request.user:
            return Response({'error': 'permission denied'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            if not request.user.check_password(request.data['old_password']):
                return Response({'error': 'Old password doesn\'t match'}, status=status.HTTP_400_BAD_REQUEST)
            print(serializer.validated_data)
            request.user.set_password(serializer.validated_data['password'])
            request.user.save()
            return Response({'message': 'Password succesfully updated', 'success': 1}, status=status.HTTP_202_ACCEPTED)
        else:
            return Response({'error': serializer.errors, "success": 0}, status=status.HTTP_400_BAD_REQUEST)
