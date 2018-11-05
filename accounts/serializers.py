from rest_framework import serializers
from django.contrib.auth.models import User
import hashlib


class UserCreateSerializer(serializers.ModelSerializer):

    email = serializers.EmailField(required=True)
    password_confirm = serializers.CharField(required=True, write_only=True)
    create = 1

    def validate(self, attrs):
        # validate username
        if User.objects.filter(username=attrs['username']):
            raise serializers.ValidationError('Username already exists!!')

        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("Enter same passwords both the times")

        if len(attrs['password']) < 8:
            raise serializers.ValidationError("Password min length: 8")

        if User.objects.filter(email=attrs['email']):
            raise serializers.ValidationError('Email already exists, choose a different one')

        return attrs

    def create(self, attrs):
        password = hashlib.sha256(attrs['password'].encode('utf-8')).hexdigest()
        user = User(username=attrs['username'], password=password,
                                        email=attrs['email'])
        user.is_active = False

        # verify the mail then change the active status of the user,
        #  by sending a mail (add to celery as a asynchronous task)

        user.save()
        return user

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password_confirm')


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'email')


# a user model with the authentication od username, email and password1, password2 for signup
#
# a home model with the temperature, humidity as fields
#
# a switch model with all the switches mapped in one to many relationship

# gas leakage, fire accident can be just api methods which on triggering performes the required action