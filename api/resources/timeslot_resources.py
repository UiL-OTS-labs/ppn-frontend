import api.rest as rest
from babel.dates import format_datetime
from django.utils.translation import get_language


class TimeSlot(rest.Resource):

    id = rest.IntegerField()

    datetime = rest.DateTimeField()

    max_places = rest.IntegerField()

    free_places = rest.IntegerField()

    def __str__(self):
        places_str = "uur"
        if self.free_places > 1:
            places_str = "uur ({} plekken resterend)".format(self.free_places)

        # Behold! The function chain FROM HELL! (Sorry)
        return format_datetime(
            self.datetime,
            'EEEE, DD-MM-YYYY, HH:MM {}',
            locale=get_language()
        ).format(
            places_str
        ).capitalize()


class TimeSlots(rest.Collection):
    class Meta:
        resource = TimeSlot
