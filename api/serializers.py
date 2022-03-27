from rest_framework import serializers
from .models import Task, User


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'


class UserRegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'name', 'password', 'password2', 'tc']
        extra_kwargs = {
            'password': {'write_only': True}
        }

        # validating password and Confirm password
        def validate(self, data):
            password = data.get('password')
            password2 = data.get('password2')
            if password != password2:
                raise serializers.ValidationError("Password and confirm password Doesn't match")
            return data

        def create(self, validate_data):
            return User.objects.create_user(**validate_data)
