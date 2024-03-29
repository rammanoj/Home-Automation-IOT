from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from django.contrib.auth.models import User


class UserCreateSerializer(serializers.ModelSerializer):

    email = serializers.EmailField(required=True)
    password_confirm = serializers.CharField(required=True, write_only=True)

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
        user = User(username=attrs['username'], email=attrs['email'])
        user.is_active = False
        user.set_password(attrs['password'])
        user.save()
        return user

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password_confirm')


class UserUpdateSerializer(serializers.ModelSerializer):

    email = serializers.EmailField(required=True)

    def validate_username(self, username):
        if User.objects.filter(username=username).exclude(id=self.instance.id).exists():
            raise serializers.ValidationError('Username already exists!!')
        return username

    def validate_email(self, email):
        if User.objects.filter(email=email).exclude(id=self.instance.id).exists():
            raise serializers.ValidationError('Email already exists!!')
        return email

    class Meta:
        model = User
        fields = ('pk', 'username', 'email')
        read_only_fields = ('pk',)


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'email')


class PasswordResetSerializer(serializers.ModelSerializer):

    confirm_password = serializers.CharField(required=True)
    old_password = serializers.CharField(required=True)

    def validate(self, attrs):
        if ('password' not in attrs) or ('confirm_password' not in attrs) or ('old_password' not in attrs):
            raise serializers.ValidationError('Fill the form completely')

        if len(attrs['password']) < 8:
            raise serializers.ValidationError('Password min length is 8')

        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError('Confirm your password correctly')

        return attrs

    class Meta:
        model = User
        fields = ('password', 'confirm_password', 'old_password')


class ResetForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)


class ForgotPasswordResetSerializer(serializers.ModelSerializer):
    password = serializers.CharField(required=True)
    confirm_new = serializers.CharField(required=True)

    def validate(self, attrs):

        if 'password' not in attrs or 'confirm_new' not in attrs:
            raise serializers.ValidationError('Fill the details completely.')

        # using self.instance you can get the current instance and exclude it on need.
        if attrs['confirm_new'] != attrs['password']:
            raise serializers.ValidationError('Enter same passwords both times')

        if len(attrs['password']) < 8:
            raise serializers.ValidationError('min password length is 8')

        return attrs

    class Meta:
        model = User
        fields = ('password', 'confirm_new')




# a user model with the authentication od username, email and password1, password2 for signup
#
# a home model with the temperature, humidity as fields
#
# a switch model with all the switches mapped in one to many relationship
# gas leakage, fire accident can be just api methods which on triggering performes the required action