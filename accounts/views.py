from django.contrib.auth import authenticate
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny

from .serializers import UserCreateSerializer, UserSerializer
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
            self.perform_create(serializer)
            message= 'We received a request to the registration from this account, please <a href=''>' \
                     'click here</a> to confirm it.'
            send_mail(
                'Verification mail at IoT',
                message,
                'rammanojpotla1608@gmail.com',
                [request.data.get('email', None)]
                )
            return Response({'result': 'Confirm the verification mail, will be sent to your mail in few minutes'})
        else:
            return Response({'errors': serializer.errors})


class UserUpdateView(generics.UpdateAPIView):
    serializer_class = UserCreateSerializer
    queryset = User.objects.all()


class UserView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        if self.get_object() != request.user:
            return Response({'error': 'Permission denied'})
        else:
            return super(UserView, self).get(self, request, *args, **kwargs)

    def get_queryset(self):
        # print(User.objects.get(user=self.request.user))
        return User.objects.all()
        # return User.objects.get(pk=self.request.pk)


@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def login(request):
    username = request.data.get('username', None)
    password = request.data.get('password', None)
    if (username is None or username == "") or (password is None or password == ""):
        return Response({'error': 'Enter valid credentails'})

    user = authenticate(username=username, password=password)
    if not user:
        return Response({'error': 'No user found as per given requirements'})

    token, tk = Token.objects.get_or_create(user=user) # if token found, use it else create new token to the user
    # tk is True on creating a new tuple,
    return Response({
        'token': token.key,
        'user': user.pk
    }, status=status.HTTP_200_OK)


def mail_verify(self):
    pass




