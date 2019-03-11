from datetime import datetime
from typing import Tuple, Union

from django import forms
from django.core.exceptions import ImproperlyConfigured, ValidationError
from django.utils.safestring import mark_safe

from api.middleware import get_current_user
from api.resources import Experiment
from api.resources.experiment_resources import ExperimentRegistration, \
    RegistrationCriteria, RegistrationCriterion
from participant.forms import BaseRegisterForm


class SpecificCriteriaValidator:

    def __init__(self, correct_value, error_message):
        self.correct_value = correct_value
        self.error_message = error_message

    def __call__(self, value):
        try:
            value = int(value)
        except ValueError:
            raise ValidationError(self.error_message)

        if value != self.correct_value:
            raise ValidationError(self.error_message)


def get_register_form(
        form: BaseRegisterForm,
        experiment: Experiment,
        allowed_fields: Union[str, list]):
    if isinstance(allowed_fields, str) and allowed_fields == '__all__':
        return _get_register_form(form, experiment)
    elif isinstance(allowed_fields, list):
        return _get_authenticated_register_form(
            form,
            experiment,
            allowed_fields
        )
    else:
        raise ImproperlyConfigured('get_register_form must be passed a list '
                                   'or "__all__" to the allowed_fields '
                                   'parameter')


def _get_register_form(form: BaseRegisterForm, experiment: Experiment):
    """This function takes a BaseRegisterForm instance and an Experiment
    instance, and returns a modified BaseRegisterForm instance containing
    extra fields, as directed by experiment criteria.
    """
    for exp_crit in experiment.specific_criteria:
        answers = exp_crit.criterion.value_list
        options = ((i, x) for i, x in enumerate(answers))

        correct_index = answers.index(exp_crit.correct_value)

        field = forms.CharField(
            label=exp_crit.criterion.name_natural,
            widget=forms.RadioSelect(
                choices=options,
            ),
            validators=[
                SpecificCriteriaValidator(
                    correct_index,
                    exp_crit.message_failed
                )
            ],
        )

        form.fields[exp_crit.criterion.name_form] = field

    timeslot_options = ((timeslot.id, str(timeslot)) for timeslot in
                        experiment.timeslots if
                        timeslot.datetime > _2_hours_ago(timeslot.datetime)
                        and timeslot.free_places > 0)

    form.fields['timeslot'] = forms.IntegerField(
        label='',
        widget=forms.RadioSelect(
            choices=timeslot_options,
        )
    )

    current_user = get_current_user()

    if not current_user.is_authenticated or not current_user.is_participant:
        form.fields['mailinglist'] = forms.BooleanField(
            label='Wil je bericht ontvangen over toekomstige taal-experimenten?',
            widget=forms.RadioSelect(
                choices=(
                    (True, 'Ja'),
                    (False, 'Nee')
                ),
            )
        )

    return form


def _get_authenticated_register_form(
        form: BaseRegisterForm,
        experiment: Experiment,
        allowed_fields: list):
    """This function takes a BaseRegisterForm instance and an Experiment
    instance, and returns a modified BaseRegisterForm instance containing
    extra fields, as directed by experiment criteria.

    This version also filters out the fields that the API doesn't need anymore.
    (This is dictated by the API, and retrieved by the frontend through a
    dedicated Resource)
    """
    form = _get_register_form(form, experiment)

    allowed_fields = set(allowed_fields + ['timeslot'])

    form_fields = [field for field in form.fields.keys()]
    for field in form_fields:
        if field not in allowed_fields:
            del form.fields[field]

    return form


def _2_hours_ago(original_dt: datetime):
    dt = datetime.now(tz=original_dt.tzinfo)
    hours = dt.hour - 2

    return dt.replace(hour=hours)


def submit_register_form(form: BaseRegisterForm, experiment: Experiment,
                         required_fields: Union[list, str], request = None) -> \
        Tuple[bool, bool, list]:
    data = form.cleaned_data

    specific_criteria = []

    if required_fields == '__all__':
        required_fields = form.fields
    elif request and request.user.is_authenticated:
        # Insert the email field from the user object
        # We need to do this for the API to get a user object and email isn't
        # provided through the form on participant account registrations.
        data['email'] = request.user.email
    else:
        # Should not happen, but just in case....
        return False, False, ['Er is iets fout gegaan!']

    for exp_crit in experiment.specific_criteria:
        name_form = exp_crit.criterion.name_form

        if name_form not in required_fields:
            continue

        criterion = RegistrationCriterion(
            name=name_form,
            value=data.pop(name_form)
        )

        specific_criteria.append(criterion)

    registration = ExperimentRegistration(**data)
    registration.specific_criteria = RegistrationCriteria(
        specific_criteria,
        is_json=False  # Instructs the collection that this is a list of
        # resources, instead of JSON from the API
    )

    response = registration.put(
        experiment=experiment.id,
        as_json=True,
    )

    messages = [mark_safe(message) for message in response.messages]

    return response.success, response.recoverable, messages
