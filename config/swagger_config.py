from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

def get_swagger_schema_view():
    """
    Returns a configured schema view for Swagger/OpenAPI documentation.
    """
    return get_schema_view(
        openapi.Info(
            title="Coding Assistant API",
            default_version='v1',
            description="""
            # Coding Assistant Backend API
            
            This API powers the Coding Assistant application, providing:
            - User authentication and management
            - Coding challenges and submissions
            - Test creation and evaluation
            - Interactive chat functionality
            
            ## Authentication
            Most endpoints require JWT authentication. Include the token in the header as:
            `Authorization: Bearer <your_token>`
            
            ## Error Codes
            - 400: Bad Request - Invalid input data
            - 401: Unauthorized - Authentication required
            - 403: Forbidden - Insufficient permissions
            - 404: Not Found - Resource not found
            - 500: Internal Server Error - Something went wrong
            """,
            terms_of_service="https://www.example.com/terms/",
            contact=openapi.Contact(email="contact@codingassistant.com"),
            license=openapi.License(name="Proprietary"),
        ),
        public=True,
        permission_classes=(permissions.AllowAny,),
    )

def get_swagger_ui_view(schema_view):
    """
    Returns a configured Swagger UI view with custom settings.
    """
    return schema_view.with_ui('swagger', cache_timeout=0)

def get_redoc_view(schema_view):
    """
    Returns a configured ReDoc view with custom settings.
    """
    return schema_view.with_ui('redoc', cache_timeout=0)
