# Rest Framework
from rest_framework import serializers

# Local App
from apps.travel.models import Destination


class DestinationBasicSerializer(serializers.ModelSerializer):
    label = serializers.CharField(source='name')
    value = serializers.CharField(source='id')

    class Meta:
        model = Destination
        fields = ('label', 'value')
