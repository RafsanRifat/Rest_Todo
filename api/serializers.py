from rest_framework import serializers
from .models import Task, User
from django.contrib.auth.models import AbstractUser
from rest_framework import serializers
from api.models import User
from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator


# from account.utils import Util


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'


class UserRegistrationSerializer(serializers.ModelSerializer):
    # We are writing this becoz we need confirm password field in our Registratin Request
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'name', 'password', 'password2', 'tc']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    # Validating Password and Confirm Password while Registration
    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        if password != password2:
            raise serializers.ValidationError("Password and Confirm Password doesn't match")
        return attrs

    def create(self, validate_data):
        return User.objects.create_user(**validate_data)


class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)

    class Meta:
        model = User
        fields = ['email', 'password']


class UserProfileViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'name']


class UserChangePasswordSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=255, style={'input_type': 'password'}, write_only=True)
    password2 = serializers.CharField(max_length=255, style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = ['password', 'password2']

    def validate(self, data):
        password = data.get('password')
        password2 = data.get('password2')
        user = self.context.get('user')
        if password != password2:
            raise serializers.ValidationError("Password and Confirm Password doesn't match")
        user.set_password(password)
        user.save()
        return data


# class SendPasswordResetEmailSerializer(serializers.Serializer):
#     email: serializers.EmailField(max_length=255)
#
#     class Meta:
#         fields = ['email']
#
#     def validate(self, data):
#         email = data.get('email')
#         print(email)
#         if User.objects.filter(email=email).exists():
#             user = User.objects.filter(email=email)
#             print(user)
#             uid = urlsafe_base64_encode(force_bytes(user.id))
#             print('Encoded id', uid)
#             token = PasswordResetTokenGenerator().make_token(user)
#             print('password reset token', token)
#             link = 'http://localhost:8000/api/resetpassword/' + uid + '/' + token
#             print('password reset link', link)
#             return data
#
#         else:
#             raise serializers.ValidationError('You are not a Registered User')
#         return super().validate(data)


class SendPasswordResetEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)

    class Meta:
        fields = ['email']

    def validate(self, attrs):
        email = attrs.get('email')
        print(email)
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uid = urlsafe_base64_encode(force_bytes(user.id))
            print('Encoded UID', uid)
            token = PasswordResetTokenGenerator().make_token(user)
            print('Password Reset Token', token)
            link = 'http://localhost:3000/api/user/reset/' + uid + '/' + token
            print('Password Reset Link', link)
            # Send EMail
            body = 'Click Following Link to Reset Your Password ' + link
            data = {
                'subject': 'Reset Your Password',
                'body': body,
                'to_email': user.email
            }
            # Util.send_email(data)
            return attrs
        else:
            raise serializers.ValidationError('You are not a Registered User')
