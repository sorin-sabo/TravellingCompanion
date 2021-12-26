# Rest Framework
from rest_framework import generics

# Local App
from apps.travel.models import Destination
from apps.travel.serializers import DestinationBasicSerializer


class DestinationBasicList(generics.ListAPIView):
    """
    Destination basic list

    * Return list of destinations using basic format.
    * Authorization: All users including guests are authorized to get list of destinations.
    """

    serializer_class = DestinationBasicSerializer
    queryset = Destination.objects.all()
