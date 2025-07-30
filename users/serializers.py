from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.utils.translation import gettext_lazy as _

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the User model.
    
    Fields:
        id: The unique identifier for the user (read-only)
        email: The email address of the user (must be unique)
        first_name: The user's first name
        last_name: The user's last name
        password: The user's password (write-only, min 8 characters)
        is_staff: Boolean indicating if the user has staff permissions (read-only)
    """
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True,
        style={'input_type': 'password'},
        label=_("Password"),
        help_text=_("At least 8 characters and can't be too common."),
    )

    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'password', 'is_staff')
        read_only_fields = ('is_staff',)
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        """Create and return a user with encrypted password"""
        return User.objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """Update a user, setting the password correctly and return it"""
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Custom token obtain serializer that includes user data in the response.
    
    Extends the default TokenObtainPairSerializer to include the serialized user
    data in the response along with the access and refresh tokens.
    """
    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)
        data['user'] = UserSerializer(self.user).data
        return data


class RegisterSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration.
    
    This serializer handles user registration, including password confirmation
    and validation.
    
    Fields:
        email: The user's email address (must be unique)
        first_name: The user's first name (required)
        last_name: The user's last name (required)
        password: The user's password (write-only, min 8 characters)
        confirm_password: Password confirmation (must match password)
    """
    password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'},
        min_length=8,
        max_length=128,
        help_text=_("At least 8 characters and can't be too common."),
    )
    confirm_password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'},
        min_length=8,
        max_length=128,
        help_text=_("Must match the password field."),
    )

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'password', 'confirm_password')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
        }

    def validate(self, attrs):
        if attrs['password'] != attrs.pop('confirm_password'):
            raise serializers.ValidationError({"password": _("Password fields didn't match.")})
        return attrs

    def create(self, validated_data):
        validated_data.pop('confirm_password', None)
        user = User.objects.create_user(**validated_data)
        return user
