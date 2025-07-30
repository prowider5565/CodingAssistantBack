from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status

def get_token_response_schema():
    return openapi.Response(
        description="Authentication successful",
        schema=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'refresh': openapi.Schema(type=openapi.TYPE_STRING, description='Refresh token for obtaining new access tokens'),
                'access': openapi.Schema(type=openapi.TYPE_STRING, description='Access token for authenticating API requests'),
                'user': openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'id': openapi.Schema(type=openapi.TYPE_INTEGER, description='User ID'),
                        'email': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_EMAIL, description='User email'),
                        'first_name': openapi.Schema(type=openapi.TYPE_STRING, description='First name'),
                        'last_name': openapi.Schema(type=openapi.TYPE_STRING, description='Last name'),
                        'is_staff': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='Staff status')
                    }
                )
            }
        ),
        examples={
            'application/json': {
                'refresh': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...',
                'access': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...',
                'user': {
                    'id': 1,
                    'email': 'user@example.com',
                    'first_name': 'John',
                    'last_name': 'Doe',
                    'is_staff': False
                }
            }
        }
    )

def get_error_response(description, errors):
    return openapi.Response(
        description=description,
        schema=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'error': openapi.Schema(type=openapi.TYPE_STRING, description='Error message'),
                'errors': openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    description='Detailed error messages',
                    additional_properties=openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Schema(type=openapi.TYPE_STRING)
                    )
                )
            }
        ),
        examples={
            'application/json': {
                'error': 'Validation Error',
                'errors': errors or {
                    'field_name': ['Error message 1', 'Error message 2']
                }
            }
        }
    )

# Common response statuses
RESPONSES = {
    '400_BAD_REQUEST': get_error_response(
        'Bad Request',
        {'field_name': ['This field is required.']}
    ),
    '401_UNAUTHORIZED': openapi.Response(
        description='Unauthorized',
        schema=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'detail': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    example='Authentication credentials were not provided.'
                )
            }
        )
    ),
    '403_FORBIDDEN': openapi.Response(
        description='Forbidden',
        schema=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'detail': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    example='You do not have permission to perform this action.'
                )
            }
        )
    ),
    '404_NOT_FOUND': openapi.Response(
        description='Not Found',
        schema=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'detail': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    example='Not found.'
                )
            }
        )
    )
}
