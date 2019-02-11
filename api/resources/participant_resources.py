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


class Appointments(rest.Collection):
    class Meta:
        path = '/api/participant/appointments/'
        supported_operations = [rest.Operations.get]
        resource = Appointment