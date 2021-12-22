# Standard Library
import logging

# Django
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings

# Local App
from apps.travel.models import Trip

# External App
from apps.core.exceptions import TransactionError

# Get an instance of a logger
logger = logging.getLogger(__name__)


# noinspection PyUnusedLocal
@receiver(post_save, sender=Trip)
def send_email_notification_on_trip_update(sender, instance, **kwargs):
    """
    Handle trip post-save event

    Upon trip post-save orchestrate:
    - Notify trip passengers that trip details got updated;
    - Log email notification event in Events
    """

    is_new = kwargs.get('created', False)

    # Send email notification only on trip update
    if not is_new:
        passengers = instance.passengers.all()
        passenger_emails = [p.email for p in passengers if p.email is not None]

        if len(passenger_emails) > 0:
            trip_name = instance.name if instance.name is not None else 'Unknown trip'
            trip_date = (
                f'{instance.start_date}'
                if instance.end_date is None
                else f'{instance.start_date}-{instance.end_date}'
            )

            trip_passengers = ''

            if passengers.count() > 1:
                for passenger in passengers:
                    if len(trip_passengers) == 0:
                        trip_passengers = ' with passengers:'
                    elif len(trip_passengers) > 0:
                        trip_passengers = f'{trip_passengers}, '

                    trip_passengers = f'{trip_passengers}{passenger.full_name}'

            trip_details = f'You have a trip: {trip_name} on {trip_date}{trip_passengers}.'

            try:
                send_mail(
                    subject=f'Trip {str(instance.name)} got updated',
                    message=trip_details,
                    from_email=settings.SERVER_EMAIL,
                    recipient_list=passenger_emails,
                    fail_silently=True
                )
            except TransactionError as exc:
                logger.error('Exception occurred saving event %s', str(exc))
