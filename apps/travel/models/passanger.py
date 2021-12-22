# Standard Library
import uuid

# Django
from django.core.validators import validate_email
from django.db import models

# External App
from apps.core.models import BaseModel, User


class Passenger(BaseModel):
    """
    Passenger mapped to authentication user as a type.
    Passengers use travel companion app to manage their trips.
    Not all passengers must be users but at least one per trip.
    Adding email to non-user passengers facilitates email notification when
    trip details get changed.
    """

    # DATABASE FIELDS
    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True
    )
    user = models.ForeignKey(
        to=User,
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )
    first_name = models.CharField(
        max_length=255,
        blank=False,
        null=False
    )
    last_name = models.CharField(
        max_length=255,
        blank=False,
        null=False
    )
    email = models.EmailField(
        max_length=254,
        blank=True,
        null=True,
        unique=True,
        validators=[validate_email]
    )

    # PROPERTIES
    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    # MANAGERS
    objects = models.Manager()

    # META CLASS
    class Meta:
        db_table = 'passenger'
        app_label = 'travel'
        verbose_name = 'Passenger'

    # TO STRING METHOD
    def __str__(self):
        return self.full_name
