# Django
from django.utils.translation import gettext_lazy as _

# Rest Framework
from rest_framework import serializers

# Local App
from apps.core.models import User


class UserRegisterSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(
        required=True,
        help_text=_('Passenger first name'))
    last_name = serializers.CharField(
        required=True,
        help_text=_('Passenger first name'))
    password = serializers.CharField(
        required=True,
        write_only=True,
        help_text=_('User password. Will be stored encrypted on 3rd party service.'))
    email = serializers.EmailField()

    class Meta:
        fields = ('first_name', 'last_name', 'email', 'password')
        model = User


class UserBasicSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('email',)
        model = User
