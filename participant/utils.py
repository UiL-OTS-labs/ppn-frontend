from datetime import datetime
from typing import List, Dict, Tuple

from django import forms
from django.core.exceptions import ValidationError

from api.middleware import get_current_user
from api.resources import Experiment
from api.resources.experiment_resources import RegistrationCriterion, \
    ExperimentRegistration, RegistrationCriteria
from api.rest import StringCollection
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


def get_register_form(form: BaseRegisterForm, experiment: Experiment):
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
                        experiment.timeslots if timeslot.datetime >
                        _2_hours_ago(timeslot.datetime))

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


def get_authenticated_register_form(
        form: BaseRegisterForm,
        experiment: Experiment,
        allowed_fields: list):
    """This function takes a BaseRegisterForm instance and an Experiment
    instance, and returns a modified BaseRegisterForm instance containing
    extra fields, as directed by experiment criteria.

    This version also filters out the fields that the API doesn't need anymore.
    """
    form = get_register_form(form, experiment)

    allowed_fields = list(allowed_fields) + ['timeslot']

    form_fields = [field for field in form.fields.keys()]
    for field in form_fields:
        if field not in allowed_fields:
            del form.fields[field]

    return form


def _2_hours_ago(original_dt: datetime):
    dt = datetime.now(tz=original_dt.tzinfo)
    hours = dt.hour - 2

    return dt.replace(hour=hours)


def submit_register_form(form: BaseRegisterForm, experiment: Experiment) -> \
        Tuple[bool, bool, StringCollection]:
    data = form.cleaned_data

    specific_criteria = []

    for exp_crit in experiment.specific_criteria:
        name_form = exp_crit.criterion.name_form

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

    return response.success, response.recoverable, response.messages
