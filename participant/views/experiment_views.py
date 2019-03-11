from braces import views as braces
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.functional import cached_property
from django.views import generic

from api.resources import Experiment
from api.resources.participant_resources import Appointments, \
    RequiredRegistrationFields
from main.mixins import OverrideLanguageMixin
from participant.forms import BaseRegisterForm
from participant.utils import get_register_form, submit_register_form


class ExperimentRegisterMixin:
    template_name = 'participant/register.html'

    def __init__(self):
        super(ExperimentRegisterMixin, self).__init__()
        self.success = None
        self.recoverable = None
        self.messages = []

    def get_context_data(self, **kwargs):
        context = super(ExperimentRegisterMixin, self).get_context_data(
            **kwargs
        )

        context['success'] = self.success
        context['recoverable'] = self.recoverable
        context['api_messages'] = self.messages
        context['experiment'] = self.experiment

        return context

    @cached_property
    def experiment(self):
        try:
            pk = self.kwargs.get('experiment')
            return Experiment.client.get(pk=pk)
        except Exception as e:
            raise ObjectDoesNotExist

    @cached_property
    def _required_fields(self):
        return '__all__'

    def form_valid(self, form):
        success, recoverable, messages = submit_register_form(
            form,
            self.experiment,
            self._required_fields,
            self.request
        )

        self.success = success
        self.recoverable = recoverable
        self.messages = messages
        return self.get(self.request, [], {})

    def get_form(self, form_class=None):
        base_form = super(ExperimentRegisterMixin, self).get_form(form_class)

        return get_register_form(
            base_form,
            self.experiment,
            self._required_fields
        )


class RegisterView(OverrideLanguageMixin,
                   ExperimentRegisterMixin,
                   generic.FormView):
    form_class = BaseRegisterForm
    language_override = 'nl'

    def dispatch(self, request, *args, **kwargs):
        try:
            # You might ask, why not just do the return in the body of this
            # if-statement. Well, that's because the very act of calling
            # self.experiment might raise ObjectDoesNotExist as well!
            # This way, we can do both in one except.
            if not self.experiment.open:
                raise ObjectDoesNotExist
        except ObjectDoesNotExist:
            return HttpResponseRedirect(
                reverse('participant:closed_experiment')
            )

        # If there's a participant logged in, redirect to the right version
        if request.user.is_authenticated and request.user.is_participant:
            args = [self.kwargs.get('experiment')]
            return HttpResponseRedirect(
                reverse('participant:register_logged_in', args=args)
            )

        return super(RegisterView, self).dispatch(request, *args, **kwargs)


class AuthenticatedRegisterView(braces.LoginRequiredMixin,
                                OverrideLanguageMixin,
                                ExperimentRegisterMixin,
                                generic.FormView):
    form_class = BaseRegisterForm
    language_override = 'nl'

    def get_context_data(self, **kwargs):
        context = super(AuthenticatedRegisterView, self).get_context_data(
            **kwargs
        )

        # Don't add anything if we are submitting the form!
        if getattr(self, 'success', False):
            return context

        appointments = Appointments.client.get()

        for appointment in appointments:
            if self.experiment.id == appointment.experiment.id:
                context['already_registered'] = True
                context['appointment'] = appointment.timeslot.datetime

                if 'messages' in context:
                    context['messages'].append('Je bent al ingeschreven voor '
                                               'dit experiment')
                else:
                    context['messages'] = [
                        'Je bent al ingeschreven voor dit experiment'
                    ]

                break

        return context

    def dispatch(self, request, *args, **kwargs):
        try:
            # You might ask, why not just do the return in the body of this
            # if-statement. Well, that's because the very act of calling
            # self.experiment might raise ObjectDoesNotExist as well!
            # This way, we can do both in one except.
            if not self.experiment.open:
                raise ObjectDoesNotExist
        except ObjectDoesNotExist:
            return HttpResponseRedirect(
                reverse('participant:closed_experiment')
            )

        # If there isn't a participant logged in, redirect to the right version
        if not request.user.is_participant:
            args = [self.kwargs.get('experiment')]
            return HttpResponseRedirect(
                reverse('participant:register', args=args)
            )

        return super(AuthenticatedRegisterView, self).dispatch(
            request,
            *args,
            **kwargs
        )

    @cached_property
    def _required_fields(self):
        fields = RequiredRegistrationFields.client.get(
            experiment=self.experiment.id
        ).fields

        return list(fields)


class ClosedExperimentView(OverrideLanguageMixin, generic.TemplateView):
    template_name = 'participant/closed_experiment.html'
    language_override = 'nl'
