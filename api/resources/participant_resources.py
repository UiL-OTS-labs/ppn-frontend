from datetime import datetime

import api.rest as rest

from .generic_resources import SuccessResponse


class MailinglistSubscribe(rest.Resource):
    class Meta:
        path = '/api/participant/subscribe_mailinglist/'
        supported_operations = [rest.Operations.put]
        default_return_resource = SuccessResponse

    email = rest.TextField()

    language = rest.TextField()

    multilingual = rest.TextField()

    dyslexic = rest.BoolField()


class SendCancelToken(rest.Resource):
    class Meta:
        path = '/api/participant/send_cancel_token/'
        supported_operations = [rest.Operations.put]
        default_return_resource = SuccessResponse

    email = rest.TextField()


class Appointment(rest.Resource):
    class Meta:
        path = '/api/participant/appointments/{pk}/'
        path_variables = ['pk']
        supported_operations = [rest.Operations.get, rest.Operations.delete]

    id = rest.IntegerField()

    creation_date = rest.DateTimeField()

    timeslot = rest.ResourceField('TimeSlot')

    experiment = rest.ResourceField('Experiment')

    @property
    def can_cancel(self) -> bool:
        # If the appointment is in the future, one can cancel
        return self.timeslot.datetime > datetime.now(
            tz=self.timeslot.datetime.tzinfo
        )


class Appointments(rest.ResourceCollection):
    class Meta:
        path = '/api/participant/appointments/'
        supported_operations = [rest.Operations.get]
        resource = Appointment


class RequiredRegistrationFields(rest.Resource):
    class Meta:
        path = '/api/participant/get_required_fields/{experiment}/'
        path_variables = ['experiment']

        supported_operations = [rest.Operations.get]

    # Yes, you can use str as a resource type. It's not a resource,
    # but what's important is that the type that is in the JSON array can be
    # put in the init function as an argument. str() vs Resource() isn't that
    # different.
    fields = rest.CollectionField(
        rest.StringCollection
    )
