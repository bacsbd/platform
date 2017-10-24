from rest_framework import serializers
from django.contrib.auth import authenticate

from .models import User, APIAuth

class RegistrationSerializer(serializers.ModelSerializer):
    """
    Serializers registration requests and creates a new user.
    """

    # Ensure passwords are at least 5 characters long, no longer than 128
    # characters, and can not be read by the client.
    password = serializers.CharField(
        max_length=128,
        min_length=5,
        write_only=True,
    )


    class Meta:
        model = User
        fields = [
            'email',
            'username',
            'password',
            'first_name',
            'last_name',
            'address',
            'institution',
            'role',
            'tshirt_size'
        ]

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=128)

    def validate(self, data):
        username = data.get('username', None)
        password = data.get('password', None)

        if username is None:
            raise serializers.ValidationError(
                'username is required to log in.'
            )

        if password is None:
            raise serializers.ValidationError(
                'password is required to log in.'
            )


        return data



class UserSerializer(serializers.ModelSerializer):
    """
    Handles searlization and deserialization of User objects.
    """

    password = serializers.CharField(
        max_length=128,
        min_length=5,
        write_only=True
    )

    class Meta:
        model = User
        fields = (
            'email',
            'username',
            'password',
            'first_name',
            'last_name',
            'address',
            'institution',
            'role',
            'tshirt_size'
        )

    def update(self, instance, validated_data):
        """
        Performs an update on a User.
        """
        _ = validated_data.pop('username', None)
        password = validated_data.pop('password', None)

        for (key, value) in validated_data.items():
            setattr(instance, key, value)

        if password is not None:
            instance.set_password(password)

        instance.save()

        return instance


class APILoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=128)
    secret_key = serializers.CharField(max_length=255)
    
    def validate(self, data):
        username = data.get('username', None)
        password = data.get('password', None)
        secret_key = data.get('secret_key', None)


        if username is None:
            raise serializers.ValidationError(
                'username is required to log in.'
            )

        if password is None:
            raise serializers.ValidationError(
                'password is required to log in.'
            )
        
        if secret_key is None:
            raise serializers.ValidationError(
                'Secret key is required'
            )
        
        apiAuth = APIAuth.objects.filter(secret=secret_key)
        
        if not apiAuth:
            raise serializers.ValidationError(
                'Secret key authentication failed.'
            )
        


        return data