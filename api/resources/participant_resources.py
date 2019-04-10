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


class ValidateMailinglistTokenResponse(rest.Resource):

    success = rest.BoolField()

    email = rest.TextField(null=True, blank=True)


class ValidateMailinglistToken(rest.Resource):
    class Meta:
        path = '/api/participant/validate_mailinglist_token/'
        supported_operations = [rest.Operations.put]
        default_return_resource = ValidateMailinglistTokenResponse

    token = rest.TextField()


class UnsubscribeFromMailinglist(rest.Resource):
    class Meta:
        path = '/api/participant/unsubscribe_from_mailinglist/'
        supported_operations = [rest.Operations.put]
        default_return_resource = SuccessResponse

    token = rest.TextField()


class SendCancelToken(rest.Resource):
    class Meta:
        path = '/api/participant/send_cancel_token/'
        supported_operations = [rest.Operations.put]
        default_return_resource = SuccessResponse

    email = rest.TextField()


class Appointment(rest.Resource):
    class Meta:
        path = '/api/participant/appointments/{id}/'
        path_variables = ['id']
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

    fields = rest.CollectionField(
        rest.StringCollection
    )


class Participant(rest.Resource):

    id = rest.IntegerField()

    name = rest.TextField()

    email = rest.TextField()

    phonenumber = rest.TextField(
        null=True,
        blank=True,
    )

    language = rest.TextField()

    multilingual = rest.BoolField()

    birth_date = rest.DateField()

    handedness = rest.TextField()

    sex = rest.TextField()

    social_status = rest.TextField()

    email_subscription = rest.BoolField()

    def get_social_status_display(self):
        if self.social_status == 'S':
            return 'Student'

        return _('Other')
