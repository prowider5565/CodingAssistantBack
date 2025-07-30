"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# Import Swagger configuration
from .swagger_config import get_swagger_schema_view, get_swagger_ui_view, get_redoc_view

# Initialize schema view
schema_view = get_swagger_schema_view()

urlpatterns = [
    # Admin site
    path('admin/', admin.site.urls),
    
    # API Documentation
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', get_swagger_ui_view(schema_view), name='schema-swagger-ui'),
    path('redoc/', get_redoc_view(schema_view), name='schema-redoc'),
    
    # API Endpoints
    path('api/auth/', include('users.urls')),
    # Add other app URLs here as you create them
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
