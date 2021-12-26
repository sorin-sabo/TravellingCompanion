"""
Advisor API Endpoints
All endpoints are prefixed with {{apiUrl}}/api/user/
"""

# Django
from django.urls import path

# Local App
from apps.core import views

urlpatterns = [
    path(
        route='register/',
        view=views.UserRegister.as_view(),
        name='register_user'
    ),

]
