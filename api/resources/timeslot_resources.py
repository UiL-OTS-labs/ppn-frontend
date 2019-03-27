from api.resources.generic_resources import SuccessResponse
from uil.core.utils import enumerate_to

import api.rest as rest
from babel.dates import format_datetime
from django.utils.translation import get_language


class TimeSlotAppointment(rest.Resource):
    """Different from the participant appointment, as this one is a child of
    a timeslot. The participant appointment has a timeslot resource as a
    child."""
    id = rest.IntegerField()

    creation_date = rest.DateTimeField()


class TimeSlotAppointments(rest.ResourceCollection):
    class Meta:
        resource = TimeSlotAppointment


class InlineTimeSlot(rest.Resource):

    id = rest.IntegerField()

    datetime = rest.DateTimeField()

    max_places = rest.IntegerField()

    free_places = rest.IntegerField()

    appointments = rest.CollectionField(TimeSlotAppointments)

    @property
    def places(self) -> list:
        """Returns a list of places with a corresponding participant (if any)"""
        appointments = self.appointments or []
        return [{
            'n':           n,
            'appointment': appointment
        } for n, appointment in enumerate_to(appointments,
                                             self.max_places, 1)]

    def has_free_places(self) -> bool:
        return self.free_places != 0

    @property
    def free_places(self) -> int:
        if self.appointments is None:
            return 0

        return self.max_places - len(self.appointments)

    def __str__(self):
        places_str = "uur"
        if self.free_places > 1:
            places_str = "uur ({} plekken resterend)".format(self.free_places)

        # Behold! The function chain FROM HELL! (Sorry)
        return format_datetime(
            self.datetime,
            'EEEE, dd-MM-YYYY, HH:mm {}',
            locale=get_language()
        ).format(
            places_str
        ).capitalize()


class InlineTimeSlots(rest.ResourceCollection):
    class Meta:
        resource = InlineTimeSlot


class TimeSlot(rest.Resource):
    class Meta:
        path = 'api/experiment/{experiment}/add_time_slot/'
        path_variables = ['experiment']
        supported_operations = [rest.Operations.put]
        default_return_resource = SuccessResponse

    experiment = rest.IntegerField()

    datetime = rest.DateTimeField()

    max_places = rest.IntegerField()


class DeleteTimeSlots(rest.Resource):
    class Meta:
        path = 'api/experiment/{experiment}/delete_time_slots/'
        path_variables = ['experiment']
        supported_operations = [rest.Operations.put]
        default_return_resource = SuccessResponse

    experiment = rest.IntegerField()

    to_delete = rest.CollectionField(rest.StringCollection)
