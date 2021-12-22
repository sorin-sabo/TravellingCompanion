# Rest Framework
from rest_framework import serializers

# Local App
from apps.travel.models import Passenger


class PassengerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Passenger
        fields = (
            'id', 'uuid', 'first_name', 'last_name', 'email',
            'user', 'created_by', 'updated_by'
        )
