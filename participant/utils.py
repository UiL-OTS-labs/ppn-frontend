from api.resources import Experiment
from participant.forms import BaseRegisterForm

from django import forms
from api.middleware import get_current_user


def get_register_form(form: BaseRegisterForm, experiment: Experiment):
    """This function takes a BaseRegisterForm instance and an Experiment
    instance, and returns a modified BaseRegisterForm instance containing
    extra fields, as directed by experiment criteria.
    """
    for exp_crit in experiment.specific_criteria:
        answers = exp_crit.criterium.value_list
        options = ((i, x) for i, x in enumerate(answers))

        field = forms.CharField(
            label=exp_crit.criterium.name_natural,
            widget=forms.RadioSelect(
                choices=options,
            )
        )

        form.fields[exp_crit.criterium.name_form] = field

    timeslot_options = ((timeslot.id, str(timeslot)) for timeslot in
                        experiment.timeslots)

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
