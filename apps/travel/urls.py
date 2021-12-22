"""
Advisor API Endpoints
All endpoints are prefixed with {{apiUrl}}/api/travel/
"""

# Django
from django.urls import path

# Local App
from apps.travel import views


urlpatterns = [
    path(
        route='trips/',
        view=views.TripView.as_view(),
        name='trips'
    ),

    path(
        route='destinations/basic/list/',
        view=views.DestinationBasicList.as_view(),
        name='destinations_basic_list'
    ),
]
