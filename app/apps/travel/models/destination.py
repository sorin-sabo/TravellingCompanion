# Django
from django.db import models

# External App
from apps.core.models import BaseModel


class Destination(BaseModel):
    """
    Destination (city) used in trip.

    """

    # DATABASE FIELDS
    code = models.CharField(
        max_length=255,
        unique=True,
        blank=False,
        null=False
    )
    name = models.CharField(
        max_length=255,
        blank=False,
        null=False
    )

    # META CLASS
    class Meta:
        db_table = 'destination'
        app_label = 'travel'
        verbose_name = 'Destination'

    # TO STRING METHOD
    def __str__(self):
        return f'{self.code} | {self.name}'
