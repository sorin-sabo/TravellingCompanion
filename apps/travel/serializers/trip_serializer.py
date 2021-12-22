# Standard Library
from datetime import datetime

# Django
from django.utils.translation import gettext_lazy as _

# Rest Framework
from rest_framework import serializers

# Local App
from apps.travel.models import Trip, Passenger, Destination


class TripPassengerSerializer(serializers.ModelSerializer):
    """
    Trip passenger serializer
    """

    name = serializers.CharField(source='full_name')

    class Meta:
        model = Passenger
        fields = (
            'id', 'name'
        )


class TripDestinationSerializer(serializers.ModelSerializer):
    """
    Trip destination serializer
    """

    class Meta:
        model = Destination
        fields = (
            'id', 'name'
        )


class TripListSerializer(serializers.ModelSerializer):
    """
    Trip list serializer
    """

    cost = serializers.DecimalField(
        max_digits=20,
        decimal_places=2,
        coerce_to_string=False
    )
    passengers = TripPassengerSerializer(many=True)
    destinations = TripDestinationSerializer(many=True)

    class Meta:
        model = Trip
        fields = (
            'name', 'cost', 'start_date', 'end_date',
            'destinations', 'passengers'
        )


class TripSaveSerializer(serializers.ModelSerializer):
    """
    Trip save serializer including custom validation
    """

    cost = serializers.DecimalField(
        required=True,
        max_digits=20,
        min_value=0,
        decimal_places=2
    )
    start_date = serializers.DateField(format="%Y-%m-%d", required=True)
    end_date = serializers.DateField(format="%Y-%m-%d", required=False)
    passengers = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Passenger.objects.all(),
        required=False
    )

    class Meta:
        model = Trip
        fields = (
            'name', 'cost', 'start_date', 'end_date',
            'passengers'
        )

    def validate(self, attrs):
        """
        Check that start date provided is a future date (>= today)
        """

        is_new = not self.instance

        if is_new:
            # Check trip start date is >= today
            start_date = attrs.get('start_date', None)

            if start_date is not None:
                today = datetime.today().date()

                if start_date < today:
                    raise serializers.ValidationError(
                        _('Trip start date must be higher or equal with current date.')
                    )

        return attrs
