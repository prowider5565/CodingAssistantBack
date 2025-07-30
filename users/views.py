from django.shortcuts import render
from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from drf_yasg.utils import swagger_auto_schema
import openapi

from .serializers import (
    UserSerializer,
    RegisterSerializer,
    CustomTokenObtainPairSerializer as TokenObtainPairSerializer,
)
from .schemas import (
    get_token_response_schema,
    RESPONSES,
    get_error_response
)

User = get_user_model()

class RegisterView(generics.CreateAPIView):
    """
    Register a new user
    
    This endpoint allows new users to register by providing their email, name, and password.
    Upon successful registration, the user will receive JWT tokens for authentication.
    """
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = RegisterSerializer
    
    @swagger_auto_schema(
        operation_description="Register a new user account",
        request_body=RegisterSerializer,
        responses={
            status.HTTP_201_CREATED: get_token_response_schema(),
            status.HTTP_400_BAD_REQUEST: get_error_response(
                'Validation Error',
                {
                    'email': ['This field is required.'],
                    'password': ['This field is required.'],
                    'confirm_password': ['This field is required.'],
                    'first_name': ['This field is required.'],
                    'last_name': ['This field is required.']
                }
            ),
        },
        tags=['Authentication']
    )

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # Generate tokens for the new user
        refresh = RefreshToken.for_user(user)
        data = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': UserSerializer(user).data
        }
        
        return Response(data, status=status.HTTP_201_CREATED)


class UserProfileView(generics.RetrieveUpdateAPIView):
    """
    get:
    Retrieve the authenticated user's profile
    
    Returns the profile information of the currently authenticated user.
    
    put:
    Update user profile
    
    Update the profile information of the currently authenticated user.
    
    patch:
    Partially update user profile
    
    Partially update the profile information of the currently authenticated user.
    """
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)
    
    @swagger_auto_schema(
        operation_description="Retrieve the authenticated user's profile",
        responses={
            status.HTTP_200_OK: UserSerializer(),
            **{k: v for k, v in RESPONSES.items() if k in ['401_UNAUTHORIZED', '403_FORBIDDEN']}
        },
        tags=['User Profile']
    )
    def get(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
        
    @swagger_auto_schema(
        operation_description="Update the authenticated user's profile",
        request_body=UserSerializer,
        responses={
            status.HTTP_200_OK: UserSerializer(),
            status.HTTP_400_BAD_REQUEST: get_error_response(
                'Validation Error',
                {'field_name': ['Error message']}
            ),
            **{k: v for k, v in RESPONSES.items() if k in ['401_UNAUTHORIZED', '403_FORBIDDEN']}
        },
        tags=['User Profile']
    )
    def put(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
        
    @swagger_auto_schema(
        operation_description="Partially update the authenticated user's profile",
        request_body=UserSerializer,
        responses={
            status.HTTP_200_OK: UserSerializer(),
            status.HTTP_400_BAD_REQUEST: get_error_response(
                'Validation Error',
                {'field_name': ['Error message']}
            ),
            **{k: v for k, v in RESPONSES.items() if k in ['401_UNAUTHORIZED', '403_FORBIDDEN']}
        },
        tags=['User Profile']
    )
    def patch(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    def get_object(self):
        return self.request.user


class LogoutView(APIView):
    """
    post:
    Logout user (blacklist refresh token)
    
    This endpoint logs out the user by blacklisting their refresh token.
    The refresh token provided in the request body will no longer be valid.
    """
    permission_classes = (permissions.IsAuthenticated,)
    
    @swagger_auto_schema(
        operation_description="Logout the user by blacklisting the refresh token",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['refresh'],
            properties={
                'refresh': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='Refresh token to blacklist'
                )
            }
        ),
        responses={
            status.HTTP_205_RESET_CONTENT: 'Successfully logged out',
            status.HTTP_400_BAD_REQUEST: get_error_response(
                'Invalid token',
                {'refresh': ['This field is required.']}
            ),
            **{k: v for k, v in RESPONSES.items() if k in ['401_UNAUTHORIZED']}
        },
        tags=['Authentication']
    )

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(
                {"error": _("Invalid token")}, 
                status=status.HTTP_400_BAD_REQUEST
            )


class CustomTokenObtainPairView(generics.GenericAPIView):
    """
    post:
    Obtain JWT token pair
    
    Authenticate a user and return JWT access and refresh tokens.
    The response includes the tokens and the user's profile information.
    """
    permission_classes = (permissions.AllowAny,)
    serializer_class = TokenObtainPairSerializer
    
    @swagger_auto_schema(
        operation_description="Obtain JWT token pair for authentication",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['email', 'password'],
            properties={
                'email': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    format=openapi.FORMAT_EMAIL,
                    description='User email address'
                ),
                'password': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    format=openapi.FORMAT_PASSWORD,
                    description='User password'
                )
            },
            example={
                'email': 'user@example.com',
                'password': 'securepassword123'
            }
        ),
        responses={
            status.HTTP_200_OK: get_token_response_schema(),
            status.HTTP_400_BAD_REQUEST: get_error_response(
                'Invalid credentials',
                {
                    'email': ['This field is required.'],
                    'password': ['This field is required.']
                }
            ),
            status.HTTP_401_UNAUTHORIZED: get_error_response(
                'Authentication failed',
                {'detail': 'No active account found with the given credentials'}
            )
        },
        tags=['Authentication']
    )

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data, status=status.HTTP_200_OK)

# Create your views here.