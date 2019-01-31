import api.rest as rest


class TimeSlot(rest.Resource):

    id = rest.IntegerField()

    datetime = rest.TextField()

    max_places = rest.IntegerField()

    free_places = rest.IntegerField()


class TimeSlots(rest.Collection):
    class Meta:
        resource = TimeSlot
