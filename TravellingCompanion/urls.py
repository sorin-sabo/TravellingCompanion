"""TravellingCompanion URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
"""

# Django documentation
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Django
from django.contrib import admin
from django.urls import path, include

# Configuration
admin.site.site_header = "Travelling Companion administration"
admin.site.site_title = "Travelling Companion administration"
admin.site.index_title = "Welcome to Travelling Companion administration"
admin.site.site_url = "/docs"

schema_view = get_schema_view(
    openapi.Info(
        title="Travelling Companion API",
        default_version='v2.0',
        description="Django 4.0 API",
        contact=openapi.Contact(email="sabo.sorin@ymail.com"),
    ),
    validators=['flex'],
    public=True,
    permission_classes=(),
    authentication_classes=()
)


# noinspection PyUnresolvedReferences
urlpatterns = [
    # API DOCUMENTATION
    path(
        route='docs/',
        view=schema_view.with_ui('redoc', cache_timeout=0),
        name='schema_redoc'
    ),

    path(
        route='admin/',
        view=admin.site.urls,
        name='admin_management'
    ),

    # CORE API
    path(
        route='api/user/',
        view=include('apps.core.urls'),
        name='user'
    ),

    # TRAVEL API
    path(
        route='api/travel/',
        view=include('apps.travel.urls'),
        name='travel'
    ),
]
