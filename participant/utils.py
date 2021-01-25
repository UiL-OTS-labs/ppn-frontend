from datetime import datetime
from typing import Tuple, Union

import requests
from django import forms
from django.core.exceptions import ImproperlyConfigured
from django.utils.safestring import mark_safe

from uil.core.middleware import get_current_user
from api.resources import Experiment
from api.resources.experiment_resources import ExperimentRegistration, \
    RegistrationCriteria, RegistrationCriterion
from participant.forms import BaseRegisterForm


def check_if_email_is_spammer(email: str) -> bool:
    url = "http://api.stopforumspam.org/api?email={}".format(email)
    response = requests.get(url)
    response_body = response.content

    # This call returns XML, however, we don't need to parse it. If the
    # string 'yes' is present, it's a spammer.
    return b'yes' in response_body


def get_register_form(
        form: BaseRegisterForm,
        experiment: Experiment,
        allowed_fields: Union[str, list]):
    if isinstance(allowed_fields, str) and allowed_fields == '__all__':
        final_form = _get_register_form(form, experiment)
    elif isinstance(allowed_fields, list):
        final_form = _get_authenticated_register_form(
            form,
            experiment,
            allowed_fields
        )
    else:
        raise ImproperlyConfigured('get_register_form must be passed a list '
                                   'or "__all__" to the allowed_fields '
                                   'parameter')
    final_form.fields['consent'] = forms.BooleanField(
        label='Dataverwerking',
        widget=forms.RadioSelect(
            choices=(
                (True, 'Ja, ik ga akkoord dat mijn gegevens worden opgeslagen '
                       't.b.v. van het verwerken van mijn aanmelding en gedeeld'
                       ' worden met de proefleider.'),
            ),
            attrs={
                'required': 'required'
            }
        ),
        required=True
    )

    return final_form


def _get_register_form(form: BaseRegisterForm, experiment: Experiment):
    """This function takes a BaseRegisterForm instance and an Experiment
    instance, and returns a modified BaseRegisterForm instance containing
    extra fields, as directed by experiment criteria.
    """
    for exp_crit in experiment.specific_criteria:
        answers = exp_crit.criterion.value_list
        options = ((i, x) for i, x in enumerate(answers))

        field = forms.CharField(
            label=exp_crit.criterion.name_natural,
            widget=forms.RadioSelect(
                choices=options,
            ),
        )

        form.fields[exp_crit.criterion.name_form] = field

    if experiment.use_timeslots:
        timeslots = sorted(experiment.timeslots, key=lambda x: x.datetime)

        timeslot_options = ((timeslot.id, str(timeslot)) for timeslot in
                            timeslots if
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
                attrs={
                    'required': 'required'
                }
            ),
            required=False
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
        data['full'] = True
    elif request and request.user.is_authenticated:
        # Insert the email field from the user object
        # We need to do this for the API to get a user object and email isn't
        # provided through the form on participant account registrations.
        data['email'] = request.user.email
        data['full'] = False
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
